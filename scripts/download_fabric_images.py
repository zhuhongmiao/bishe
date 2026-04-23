import csv
import pathlib
import random
import sys
import time
from typing import Iterable, Optional

import requests

API_DETAIL = 'https://api.swatchon.com/api/mall/v1/qualities/{id}'
TIMEOUT = 30
PROGRESS_EVERY = 50
IMAGE_SUFFIXES = ['.jpg', '.jpeg', '.png', '.webp']
MAX_RETRIES = 4
BASE_DELAY_SECONDS = 1.5
LONG_DELAY_ON_403_SECONDS = 12


def iter_ids_from_csv(csv_path: pathlib.Path) -> Iterable[str]:
    with csv_path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fabric_id = str(row.get('id', '')).strip()
            if fabric_id:
                yield fabric_id


def pick_image_url(detail: dict) -> Optional[str]:
    medias = detail.get('medias') or []
    for media in medias:
        thumbnail = media.get('thumbnail')
        if thumbnail:
            return thumbnail
    for media in medias:
        path = media.get('path', '')
        if isinstance(path, str) and path.lower().endswith(tuple(IMAGE_SUFFIXES)):
            return path
    return None


def local_image_exists(output_dir: pathlib.Path, fabric_id: str) -> bool:
    return any((output_dir / f'{fabric_id}{suffix}').exists() for suffix in IMAGE_SUFFIXES)


def sleep_with_jitter(seconds: float) -> None:
    time.sleep(seconds + random.uniform(0.2, 0.8))


def fetch_detail_with_retry(session: requests.Session, fabric_id: str) -> tuple[Optional[dict], str]:
    last_status = 'unknown-error'
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(API_DETAIL.format(id=fabric_id), timeout=TIMEOUT)
            if response.status_code == 403:
                last_status = '403-forbidden'
                sleep_with_jitter(LONG_DELAY_ON_403_SECONDS * attempt)
                continue
            response.raise_for_status()
            return response.json(), 'ok'
        except requests.HTTPError as exc:
            last_status = f'http-{exc.response.status_code}' if exc.response is not None else 'http-error'
        except requests.RequestException:
            last_status = 'network-error'

        sleep_with_jitter(BASE_DELAY_SECONDS * attempt)

    return None, last_status


def download_binary_with_retry(session: requests.Session, image_url: str) -> tuple[Optional[bytes], str]:
    last_status = 'unknown-error'
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(image_url, timeout=TIMEOUT)
            if response.status_code == 403:
                last_status = '403-image-forbidden'
                sleep_with_jitter(LONG_DELAY_ON_403_SECONDS * attempt)
                continue
            response.raise_for_status()
            return response.content, 'ok'
        except requests.HTTPError as exc:
            last_status = f'http-image-{exc.response.status_code}' if exc.response is not None else 'http-image-error'
        except requests.RequestException:
            last_status = 'image-network-error'

        sleep_with_jitter(BASE_DELAY_SECONDS * attempt)

    return None, last_status


def download_image(session: requests.Session, fabric_id: str, output_dir: pathlib.Path) -> tuple[bool, str]:
    if local_image_exists(output_dir, fabric_id):
        return True, 'exists'

    detail, detail_status = fetch_detail_with_retry(session, fabric_id)
    if not detail:
        return False, detail_status

    image_url = pick_image_url(detail)
    if not image_url:
        return False, 'missing-media'

    image_bytes, image_status = download_binary_with_retry(session, image_url)
    if not image_bytes:
        return False, image_status

    suffix = pathlib.Path(image_url.split('?')[0]).suffix or '.jpg'
    target_path = output_dir / f'{fabric_id}{suffix}'
    target_path.write_bytes(image_bytes)
    return True, 'saved'


def main() -> int:
    workspace_root = pathlib.Path(__file__).resolve().parents[1]
    csv_path = workspace_root / 'BE' / 'BE' / 'apps' / 'analysis' / 'data.csv'
    output_dir = workspace_root / 'FE' / 'public' / 'fabrics'
    missing_path = workspace_root / 'download_fabric_missing_ids.txt'
    output_dir.mkdir(parents=True, exist_ok=True)

    ids = list(iter_ids_from_csv(csv_path))
    if not ids:
        print('No ids found in CSV.')
        return 1

    if len(sys.argv) > 1:
        ids = ids[: int(sys.argv[1])]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.swatchon.com/fabric',
        'Origin': 'https://www.swatchon.com',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }

    saved = 0
    existing = 0
    missing: list[str] = []
    errors = 0
    total = len(ids)

    with requests.Session() as session:
        session.headers.update(headers)
        for index, fabric_id in enumerate(ids, start=1):
            try:
                ok, status = download_image(session, fabric_id, output_dir)
                if ok and status == 'saved':
                    saved += 1
                elif ok and status == 'exists':
                    existing += 1
                else:
                    missing.append(fabric_id)
                    print(f'[skip] {fabric_id}: {status}')
            except Exception as exc:
                errors += 1
                missing.append(fabric_id)
                print(f'[error] {fabric_id}: {exc}')

            if index % PROGRESS_EVERY == 0 or index == total:
                print(
                    f'[progress] {index}/{total} | saved={saved} existing={existing} '
                    f'missing={len(missing)} errors={errors}'
                )

            sleep_with_jitter(BASE_DELAY_SECONDS)

    missing_path.write_text('\n'.join(missing), encoding='utf-8')
    print(
        f'Finished. total={total} saved={saved} existing={existing} missing={len(missing)} '
        f'errors={errors} output={output_dir} missing_list={missing_path}'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
