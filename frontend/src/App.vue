<template>
  <div class="container">
    <h1>Pvue - Vue3 + Python WebSocket</h1>
    
    <!-- 插件演示区域 -->
    <div class="plugin-demo-section">
      <h2>插件系统演示</h2>
      
      <div class="demo-buttons">
        <!-- 权限控制插件演示 -->
        <div class="demo-group">
          <h3>权限控制</h3>
          <button v-permission="'read'" class="demo-btn">读权限可见</button>
          <button v-permission="'write'" class="demo-btn">写权限可见</button>
          <button v-role="'admin'" class="demo-btn admin-btn">管理员可见</button>
          <button @click="toggleWritePermission" class="demo-btn">切换写权限</button>
          <button @click="toggleAdminRole" class="demo-btn">切换管理员角色</button>
        </div>
        
        <!-- 消息通知插件演示 -->
        <div class="demo-group">
          <h3>消息通知</h3>
          <button @click="showSuccessNotification" class="demo-btn success-btn">成功通知</button>
          <button @click="showErrorNotification" class="demo-btn error-btn">错误通知</button>
          <button @click="showWarningNotification" class="demo-btn warning-btn">警告通知</button>
          <button @click="showInfoNotification" class="demo-btn info-btn">信息通知</button>
        </div>
      </div>
    </div>
    
    <!-- 功能选择 -->
    <div class="function-selector">
      <label>选择处理功能：</label>
      <select v-model="selectedFunction">
        <option value="uppercase">转大写</option>
        <option value="lowercase">转小写</option>
        <option value="reverse">反转字符串</option>
      </select>
    </div>
    
    <!-- 输入区域 -->
    <div class="input-section">
      <input 
        type="text" 
        v-model="inputText" 
        placeholder="请输入文本..."
        @keyup.enter="sendMessage"
        :disabled="isLoading"
      >
      <button @click="sendMessage" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        {{ isLoading ? '处理中...' : '提交' }}
      </button>
      <button @click="clearAll" class="clear-btn">清空</button>
    </div>
    
    <!-- 消息历史记录 -->
    <div class="history-section">
      <h2>消息历史</h2>
      <div class="history-list">
        <div 
          v-for="(item, index) in messageHistory" 
          :key="index" 
          class="history-item"
        >
          <div class="history-input">
            <strong>输入：</strong>{{ item.input }}
            <span class="history-function">{{ item.function }}</span>
          </div>
          <div class="history-result">
            <strong>结果：</strong>{{ item.result }}
          </div>
        </div>
        <div v-if="messageHistory.length === 0" class="no-history">
          暂无消息记录
        </div>
      </div>
    </div>
    
    <!-- 当前结果 -->
    <div class="result-section">
      <h2>当前结果</h2>
      <div class="result-box">{{ currentResult }}</div>
    </div>
    
    <!-- 状态显示 -->
    <div class="status" :class="statusClass">
      {{ statusMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// 导入插件钩子
import { usePermission } from './plugins/permission'
import { useNotification } from './plugins/notification'

// 插件API
const permission = usePermission()
const notify = useNotification()

// 原有WebSocket功能状态
const inputText = ref('')
const currentResult = ref('')
const statusMessage = ref('正在连接WebSocket...')
const statusClass = ref('')
const isLoading = ref(false)
const selectedFunction = ref('uppercase')
const messageHistory = ref([])
let ws = null

// 连接WebSocket
const connectWebSocket = () => {
  try {
    // WebSocket服务器地址
    ws = new WebSocket('ws://localhost:8765')
    
    ws.onopen = () => {
      statusMessage.value = 'WebSocket连接成功'
      statusClass.value = 'success'
      notify.success('WebSocket连接成功！', { title: '连接状态' })
    }
    
    ws.onmessage = (event) => {
      const response = JSON.parse(event.data)
      currentResult.value = response.result
      
      // 添加到历史记录
      messageHistory.value.unshift({
        input: inputText.value,
        function: selectedFunction.value,
        result: response.result
      })
      
      // 限制历史记录数量
      if (messageHistory.value.length > 10) {
        messageHistory.value.pop()
      }
      
      statusMessage.value = '消息处理完成'
      statusClass.value = 'success'
      isLoading.value = false
    }
    
    ws.onerror = (error) => {
      statusMessage.value = `WebSocket错误: ${error.message}`
      statusClass.value = 'error'
      isLoading.value = false
      notify.error(`WebSocket错误: ${error.message}`, { title: '连接错误' })
    }
    
    ws.onclose = () => {
      statusMessage.value = 'WebSocket连接已关闭'
      statusClass.value = 'error'
      isLoading.value = false
      notify.warning('WebSocket连接已关闭，正在尝试重连...', { title: '连接状态' })
      // 尝试重连
      setTimeout(connectWebSocket, 3000)
    }
  } catch (error) {
    statusMessage.value = `连接失败: ${error.message}`
    statusClass.value = 'error'
    isLoading.value = false
    notify.error(`连接失败: ${error.message}`, { title: '连接错误' })
  }
}

// 发送消息到后端
const sendMessage = () => {
  if (!inputText.value.trim()) {
    statusMessage.value = '请输入要处理的文本'
    statusClass.value = 'error'
    notify.warning('请输入要处理的文本！', { title: '输入提示' })
    return
  }
  
  if (ws && ws.readyState === WebSocket.OPEN) {
    const message = {
      text: inputText.value,
      function: selectedFunction.value
    }
    ws.send(JSON.stringify(message))
    statusMessage.value = '消息发送中...'
    statusClass.value = ''
    isLoading.value = true
    notify.info('正在处理您的请求...', { title: '处理中' })
  } else {
    statusMessage.value = 'WebSocket未连接'
    statusClass.value = 'error'
    notify.error('WebSocket未连接，请稍后重试！', { title: '连接错误' })
  }
}

// 清空所有内容
const clearAll = () => {
  inputText.value = ''
  currentResult.value = ''
  messageHistory.value = []
  statusMessage.value = '已清空所有内容'
  statusClass.value = 'success'
  notify.success('已清空所有内容！', { title: '操作成功' })
}

// 权限控制演示方法
const toggleWritePermission = () => {
  const hasWritePermission = permission.check('write')
  if (hasWritePermission) {
    permission.removePermission('write')
    notify.warning('写权限已移除！', { title: '权限变更' })
  } else {
    permission.addPermission('write')
    notify.success('写权限已添加！', { title: '权限变更' })
  }
}

const toggleAdminRole = () => {
  const isAdmin = permission.checkRole('admin')
  if (isAdmin) {
    permission.removePermission('admin')
    notify.warning('管理员角色已移除！', { title: '角色变更' })
  } else {
    permission.addPermission('admin')
    notify.success('管理员角色已添加！', { title: '角色变更' })
  }
}

// 消息通知演示方法
const showSuccessNotification = () => {
  notify.success('操作成功！', {
    title: '成功',
    duration: 2000
  })
}

const showErrorNotification = () => {
  notify.error('操作失败，请重试！', {
    title: '错误',
    duration: 5000
  })
}

const showWarningNotification = () => {
  notify.warning('请注意，这是一个警告！', {
    title: '警告',
    position: 'top-left'
  })
}

const showInfoNotification = () => {
  notify.info('这是一条提示信息！', {
    title: '信息',
    closeable: false
  })
}

// 组件挂载时连接WebSocket
onMounted(() => {
  connectWebSocket()
})

// 组件卸载前关闭WebSocket连接
onBeforeUnmount(() => {
  if (ws) {
    ws.close()
  }
})
</script>