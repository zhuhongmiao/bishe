<template>
  <div class="min-h-screen bg-[#f5f5f5] px-5 pb-10 pt-4 text-slate-900">
    <div v-if="loading" class="detail-shell detail-state">正在加载面料信息...</div>

    <div v-else-if="!fabric" class="detail-shell detail-state">未获取到面料信息</div>

    <div v-else class="detail-shell">
      <button type="button" class="back-link" @click="router.back()">← 返回首页</button>

      <div class="detail-grid">
        <div class="detail-cover">
          <img :src="imageUrl" alt="fabric" class="cover-image" />
        </div>

        <div class="detail-main">
          <div class="detail-head">
            <div>
              <div class="detail-tag">Fabric Detail / 面料详情</div>
              <h1 class="detail-title">{{ formatBilingualValue(fabric.title) }}</h1>
            </div>
            <div class="detail-price">
              <span class="detail-price-label">价格 / Price</span>
              <span class="detail-price-value">{{ fabric.price }}</span>
            </div>
          </div>

          <div class="detail-info-grid">
            <div v-for="field in baseFields" :key="field.label" class="info-card">
              <div class="info-label">{{ field.label }}</div>
              <div class="info-value">{{ field.value }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '@/api'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { FIELD_LABELS, formatBilingualValue } from '@/utils/bilingual'

const route = useRoute()
const router = useRouter()
const fabric = ref(null)
const loading = ref(true)

const imageUrl = computed(() => getItemImage(route.params.id))

const baseFields = computed(() => {
  if (!fabric.value) return []

  return [
    { label: '编号 / ID', value: fabric.value.id ?? '暂无 / N/A' },
    { label: FIELD_LABELS.title, value: formatBilingualValue(fabric.value.title) },
    { label: FIELD_LABELS.category_name, value: formatBilingualValue(fabric.value.category_name) },
    { label: FIELD_LABELS.category_id, value: fabric.value.category_id ?? '暂无 / N/A' },
    { label: FIELD_LABELS.weight, value: fabric.value.weight ?? '暂无 / N/A' },
    { label: FIELD_LABELS.country, value: formatBilingualValue(fabric.value.country) },
    { label: FIELD_LABELS.pattern, value: formatBilingualValue(fabric.value.pattern) },
    { label: FIELD_LABELS.like, value: fabric.value.like ?? '暂无 / N/A' },
  ]
})
const getItemImage = (id) => {
  const MIN = 1
  const MAX = 4896
  const RANGE = MAX - MIN + 1

  const str = String(id)

  // FNV-1a 32位哈希
  let hash = 2166136261

  for (let i = 0; i < str.length; i++) {
    hash ^= str.charCodeAt(i)
    hash = Math.imul(hash, 16777619)
  }

  // 转成无符号整数
  hash = hash >>> 0

  const imgNum= MIN + (hash % RANGE)
  return `/fabrics/${imgNum}.jpg`
}
const getFabricDetail = async () => {
  loading.value = true
  try {
    const res = await api.fabricDetail(route.params.id)
    fabric.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  getFabricDetail()
})
</script>

<style scoped>
.detail-shell {
  margin: 0 auto;
  max-width: 1320px;
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 32px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.06);
  padding: 28px;
}

.detail-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 360px;
  color: #64748b;
  font-size: 16px;
}

.back-link {
  margin-bottom: 20px;
  border: none;
  background: transparent;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1.05fr 1.15fr;
  gap: 28px;
}

.detail-cover {
  overflow: hidden;
  border-radius: 28px;
  background: #e2e8f0;
  min-height: 520px;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.detail-main {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.detail-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  padding-bottom: 22px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.9);
}

.detail-tag {
  color: #64748b;
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.detail-title {
  margin-top: 12px;
  font-size: 36px;
  line-height: 1.2;
  font-weight: 600;
  color: #0f172a;
}

.detail-subtitle {
  margin-top: 14px;
  max-width: 560px;
  color: #64748b;
  font-size: 15px;
  line-height: 1.8;
}

.detail-price {
  min-width: 140px;
  border-radius: 24px;
  background: #f8fafc;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-price-label {
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #94a3b8;
}

.detail-price-value {
  font-size: 30px;
  font-weight: 600;
  color: #0f172a;
}

.detail-info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.info-card {
  border-radius: 24px;
  background: #f8fafc;
  padding: 18px 20px;
}

.info-label {
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #94a3b8;
}

.info-value {
  margin-top: 10px;
  color: #0f172a;
  font-size: 18px;
  line-height: 1.6;
  word-break: break-word;
}

@media (max-width: 1100px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .detail-cover {
    min-height: 400px;
  }
}

@media (max-width: 768px) {
  .detail-shell {
    padding: 20px;
    border-radius: 24px;
  }

  .detail-head {
    flex-direction: column;
  }

  .detail-title {
    font-size: 28px;
  }

  .detail-info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
