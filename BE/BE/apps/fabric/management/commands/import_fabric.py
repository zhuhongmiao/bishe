# apps/febric/management/commands/import_febric.py
import csv
import random
from decimal import Decimal, InvalidOperation
from typing import Iterable, Tuple

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import F
from apps.fabric.models import Fabric


DEFAULT_UNIQUE_FIELDS = (
    "title", "category_name", "category_id", "weight", "country", "price", "pattern"
)


def to_int(v, default=None):
    if v is None:
        return default
    s = str(v).strip()
    if s == "":
        return default
    try:
        return int(s)
    except ValueError:
        return default


def to_dec(v, default=Decimal("0.00")):
    if v is None:
        return default
    s = str(v).strip()
    if s == "":
        return default
    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return default


def row_signature(row: dict, fields: Tuple[str, ...]) -> Tuple:
    """Build a tuple signature used to dedupe/update."""
    sig = []
    for f in fields:
        val = row.get(f)
        if f in ("category_id", "weight"):
            sig.append(to_int(val))
        elif f == "price":
            sig.append(to_dec(val))
        else:
            sig.append((val or "").strip())
    return tuple(sig)


class Command(BaseCommand):
    help = (
        "Import CSV into Febric table.\n"
        "- Default: fast batch insert with random `like` 0–399.\n"
        "- Optional: --dedupe to avoid duplicates by composite key.\n"
        "- Optional: --update to update matched rows instead of skipping (with --dedupe).\n"
        "Required headers: title,category_name,category_id,weight,country,price,pattern"
    )

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to CSV file")
        parser.add_argument(
            "--encoding", default="utf-8", help="CSV encoding (default utf-8)"
        )
        parser.add_argument(
            "--batch", type=int, default=5000, help="Bulk batch size (default 5000)"
        )
        parser.add_argument(
            "--dedupe",
            action="store_true",
            help="Dedupe by composite key (default key uses all business fields).",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="When used with --dedupe, update matched rows instead of skipping.",
        )
        parser.add_argument(
            "--unique-fields",
            type=str,
            default=",".join(DEFAULT_UNIQUE_FIELDS),
            help=(
                "Comma-separated field list for composite unique key. "
                f"Default: {','.join(DEFAULT_UNIQUE_FIELDS)}"
            ),
        )
        parser.add_argument(
            "--keep-like",
            action="store_true",
            help="If CSV has `like` column and you want to keep it; otherwise randomize.",
        )

    def handle(self, *args, **opts):
        path = opts["csv_path"]
        encoding = opts["encoding"]
        batch_size = opts["batch"]
        dedupe = opts["dedupe"]
        update_on_match = opts["update"]
        keep_like = opts["keep_like"]
        unique_fields = tuple(
            f.strip()
            for f in (opts["unique_fields"].split(",") if opts["unique_fields"] else [])
            if f.strip()
        )
        if not unique_fields:
            unique_fields = DEFAULT_UNIQUE_FIELDS

        # 1) 读取 CSV（流式）
        try:
            f = open(path, "r", encoding=encoding, newline="")
        except FileNotFoundError:
            raise CommandError(f"File not found: {path}")
        except UnicodeDecodeError:
            raise CommandError(
                f"Wrong encoding for {path}. Try --encoding gbk or --encoding utf-8-sig"
            )

        with f:
            reader = csv.DictReader(reader_line for reader_line in f)
            header = reader.fieldnames or []
            required = [
                "title",
                "category_name",
                "category_id",
                "weight",
                "country",
                "price",
                "pattern",
            ]
            missing = [h for h in required if h not in header]
            if missing:
                raise CommandError(f"CSV missing columns: {missing}")

            # 2) 如果需要去重/更新，先构建 DB 中已存在数据的签名映射（signature -> id）
            existing_map = {}
            if dedupe:
                self.stdout.write(self.style.WARNING("Building existing index ..."))
                # 仅取到去重用到的字段，减少内存
                values = list(unique_fields) + ["id"]
                # 注意：如果表非常大，这一步会较慢；你的数据量（2万+）是可以接受的
                for rec in Fabric.objects.all().values(*values):
                    sig = tuple(
                        rec[f] if f != "price" else to_dec(rec[f]) for f in unique_fields
                    )
                    existing_map[sig] = rec["id"]
                self.stdout.write(
                    self.style.SUCCESS(f"Existing rows indexed: {len(existing_map)}")
                )

            to_create = []
            to_update = []
            created = 0
            updated = 0
            processed = 0

            def flush():
                nonlocal to_create, to_update, created, updated
                if to_create:
                    Fabric.objects.bulk_create(to_create, batch_size=batch_size)
                    created += len(to_create)
                    to_create = []
                if to_update:
                    Fabric.objects.bulk_update(
                        to_update,
                        fields=[
                            "title",
                            "category_name",
                            "category_id",
                            "weight",
                            "country",
                            "price",
                            "pattern",
                            "like",
                            "updated_at",
                        ],
                        batch_size=batch_size,
                    )
                    updated += len(to_update)
                    to_update = []

            for r in reader:
                processed += 1

                data = {
                    "title": (r.get("title") or "").strip(),
                    "category_name": (r.get("category_name") or "").strip(),
                    "category_id": to_int(r.get("category_id"), 0) or 0,
                    "weight": to_int(r.get("weight")),
                    "country": (r.get("country") or "").strip(),
                    "price": to_dec(r.get("price")),
                    "pattern": (r.get("pattern") or "").strip(),
                }

                # like：若 CSV 提供且 --keep-like，则用 CSV；否则随机 0–399
                if keep_like and "like" in r and str(r.get("like") or "").strip() != "":
                    try:
                        data["like"] = max(0, int(str(r["like"]).strip()))
                    except ValueError:
                        data["like"] = random.randint(0, 399)
                else:
                    data["like"] = random.randint(0, 399)

                if dedupe:
                    sig = row_signature(r, unique_fields)
                    existing_id = existing_map.get(sig)
                    if existing_id:
                        if update_on_match:
                            obj = Fabric(id=existing_id, **data)
                            to_update.append(obj)
                        # 若不更新，则跳过
                    else:
                        obj = Fabric(**data)
                        to_create.append(obj)
                        # 新建后，把 sig 标记到 existing_map，避免本次导入内重复
                        existing_map[sig] = -1  # 临时占位
                else:
                    # 不去重：直接创建
                    obj = Fabric(**data)
                    to_create.append(obj)

                if (len(to_create) + len(to_update)) >= batch_size:
                    flush()

            # 尾批次提交
            flush()

        self.stdout.write(
            self.style.SUCCESS(
                f"Import finished. Processed: {processed}, Created: {created}, Updated: {updated}"
            )
        )
