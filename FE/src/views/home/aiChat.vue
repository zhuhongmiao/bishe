<template>
  <div class="chat-container">
    <!-- 顶部标题栏 -->
    <div class="header">
      <div>
        <h1 class="text-2xl font-bold">AI问答 · 布料智能助手</h1>
        <p class="text-sm opacity-90 mt-1">
          结合历史数据与大模型，为你解答布料价格、趋势与市场相关问题。
        </p>
      </div>
      <div class="flex items-center gap-4 text-sm">
        <div class="flex items-center gap-2">
          <span>联网搜索</span>
          <a-switch v-model:checked="enableWebSearch" size="small" />
        </div>
        <div class="flex items-center gap-2">
          <span>深度思考</span>
          <a-switch v-model:checked="enableDeepThinking" size="small" />
        </div>
      </div>
    </div>

    <!-- 主聊天区域 -->
    <div class="main-content">
      <!-- 消息列表区域 -->
      <div ref="scrollRef" class="messages-area">
        <div class="messages-container">
          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="message-wrapper"
            :class="msg.role === 'user' ? 'user-message' : 'assistant-message'"
          >
            <div
              class="message-bubble"
              :class="msg.role === 'user' ? 'user-bubble' : 'assistant-bubble'"
            >
              <div class="message-text">
                {{ msg.content }}
              </div>
            </div>
          </div>
          
          <div v-if="loading" class="message-wrapper assistant-message">
            <div class="loading-bubble">
              正在思考中，请稍候…
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-container">
          <div class="input-hint">
            小提示：可以直接提问「当前某类布料的大致价格区间？」或「不同国家之间的价格差异？」等问题。
          </div>
          <div class="input-wrapper">
            <a-textarea
              v-model:value="input"
              :auto-size="{ minRows: 2, maxRows: 4 }"
              placeholder="请输入你的问题，回车发送，Shift+回车换行"
              class="chat-textarea"
              @keydown.enter.prevent="handleEnter"
            />
            <a-button 
              type="primary" 
              size="large"
              :loading="loading" 
              class="send-button"
              @click="handleSend"
            >
              发送
            </a-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, nextTick, useTemplateRef } from 'vue'
import api from '@/api'

const info = inject('info')

const messages = ref([
  {
    role: 'assistant',
    content:
      '你好，我是布料智能分析助手。\n你可以问我关于布料价格区间、不同国家/图案的价格差异、克重对价格影响等问题，我会结合历史数据和大模型能力为你解答。',
  },
])

const input = ref('')
const loading = ref(false)
const enableWebSearch = ref(false)
const enableDeepThinking = ref(false)

const scrollRef = useTemplateRef('scrollRef')

const scrollToBottom = async () => {
  await nextTick()
  if (scrollRef.value) {
    const el = scrollRef.value
    el.scrollTop = el.scrollHeight
  }
}

const handleEnter = (event) => {
  if (event.shiftKey) {
    input.value += '\n'
    return
  }
  handleSend()
}

const handleSend = async () => {
  const text = input.value.trim()
  if (!text) {
    info('请输入问题', 'warning')
    return
  }
  if (loading.value) {
    return
  }

  messages.value.push({
    role: 'user',
    content: text,
  })
  input.value = ''
  scrollToBottom()

  loading.value = true

  const assistantMessageIndex = messages.value.length
  messages.value.push({
    role: 'assistant',
    content: '',
  })

  try {
    await api.aiChatStream(
      {
        question: text,
        enable_web_search: enableWebSearch.value,
        enable_deep_thinking: enableDeepThinking.value,
      },
      (chunk) => {
        messages.value[assistantMessageIndex].content += chunk
        scrollToBottom()
      }
    )
  } catch (error) {
    messages.value.splice(assistantMessageIndex, 1)
    
    api
      .aiChat({
        question: text,
        enable_web_search: enableWebSearch.value,
        enable_deep_thinking: enableDeepThinking.value,
      })
      .then((res) => {
        if (res.data.code === 200 && res.data.data && res.data.data.answer) {
          messages.value.push({
            role: 'assistant',
            content: res.data.data.answer,
          })
        } else {
          info(res.data.msg || 'AI 回答失败', 'error')
        }
      })
      .catch(() => {
        info('AI 请求失败，请稍后重试', 'error')
      })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.chat-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f9fafb;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: linear-gradient(to right, #3b82f6, #6366f1);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem 1rem;
  max-height: calc(100vh - 250px);
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.messages-area::-webkit-scrollbar {
  display: none;
}

.messages-container {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.message-wrapper {
  display: flex;
}

.user-message {
  justify-content: flex-end;
}

.assistant-message {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 75%;
  padding: 1.25rem;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-bubble {
  background: #3b82f6;
  color: white;
  border-bottom-right-radius: 0.25rem;
}

.assistant-bubble {
  background: white;
  color: #1f2937;
  border: 1px solid #e5e7eb;
  border-bottom-left-radius: 0.25rem;
}

.message-text {
  font-size: 1rem;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.loading-bubble {
  background: white;
  border: 2px dashed #93c5fd;
  color: #3b82f6;
  padding: 0.75rem 1.25rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input-area {
  border-top: 1px solid #e5e7eb;
  background: white;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}

.input-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1rem;
}

.input-hint {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 0.75rem;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
}

.chat-textarea {
  flex: 1;
}

.send-button {
  flex-shrink: 0;
  height: auto;
  padding: 0.5rem 2rem;
}
</style>
