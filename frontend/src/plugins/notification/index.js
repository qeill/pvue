import { inject, provide, ref, h, createApp } from 'vue'
import './style.css'

// 注入键
const NOTIFICATION_KEY = Symbol('notification')

// 通知组件
const NotificationComponent = {
  props: ['notification'],
  setup(props) {
    const handleClose = () => {
      props.notification.onClose()
    }
    
    return () => h('div', {
      class: [
        'notification',
        `notification-${props.notification.type}`,
        `notification-${props.notification.position}`
      ],
      style: {
        animation: props.notification.visible ? 'notification-slide-in 0.3s ease-out forwards' : 'notification-slide-out 0.3s ease-in forwards'
      }
    }, [
      h('div', { class: 'notification-content' }, [
        h('div', { class: 'notification-message' }, props.notification.message),
        props.notification.title && h('div', { class: 'notification-title' }, props.notification.title)
      ]),
      h('button', {
        class: 'notification-close',
        onClick: handleClose
      }, '×')
    ])
  }
}

// 消息通知插件
const NotificationPlugin = {
  name: 'notification',
  
  // 安装方法
  install(app, options = {}) {
    // 默认配置
    const defaultOptions = {
      duration: 3000,
      position: 'top-right',
      closeable: true
    }
    
    // 合并配置
    const config = { ...defaultOptions, ...options }
    
    // 通知列表
    const notifications = ref([])
    
    // 创建通知容器
    const container = document.createElement('div')
    container.className = 'notification-container'
    document.body.appendChild(container)
    
    // 创建通知应用实例
    const notificationApp = createApp({})
    notificationApp.mount(container)
    
    // 显示通知
    const showNotification = (type, message, options = {}) => {
      // 生成唯一ID
      const id = Date.now() + Math.random().toString(36).substr(2, 9)
      
      // 合并选项
      const notificationOptions = { ...config, ...options }
      
      // 创建通知对象
      const notification = {
        id,
        type,
        message,
        title: notificationOptions.title,
        position: notificationOptions.position,
        duration: notificationOptions.duration,
        closeable: notificationOptions.closeable,
        visible: true,
        onClose: () => {
          closeNotification(id)
        }
      }
      
      // 添加到通知列表
      notifications.value.push(notification)
      
      // 渲染通知
      renderNotification(notification)
      
      // 设置自动关闭
      if (notification.duration > 0) {
        setTimeout(() => {
          closeNotification(id)
        }, notification.duration)
      }
      
      return id
    }
    
    // 渲染单个通知
    const renderNotification = (notification) => {
      // 创建通知根元素
      const notificationEl = document.createElement('div')
      notificationEl.id = `notification-${notification.id}`
      container.appendChild(notificationEl)
      
      // 渲染通知组件
      const app = createApp(NotificationComponent, { notification })
      app.mount(notificationEl)
      
      // 保存应用实例
      notification.app = app
    }
    
    // 关闭通知
    const closeNotification = (id) => {
      const index = notifications.value.findIndex(n => n.id === id)
      if (index !== -1) {
        const notification = notifications.value[index]
        notification.visible = false
        
        // 等待动画结束后移除
        setTimeout(() => {
          // 卸载应用
          if (notification.app) {
            notification.app.unmount()
          }
          
          // 移除DOM元素
          const el = document.getElementById(`notification-${id}`)
          if (el) {
            el.remove()
          }
          
          // 从列表中移除
          notifications.value.splice(index, 1)
        }, 300)
      }
    }
    
    // 关闭所有通知
    const closeAllNotifications = () => {
      notifications.value.forEach(notification => {
        closeNotification(notification.id)
      })
    }
    
    // 通知方法
    const notificationMethods = {
      // 显示成功通知
      success(message, options) {
        return showNotification('success', message, options)
      },
      
      // 显示错误通知
      error(message, options) {
        return showNotification('error', message, options)
      },
      
      // 显示警告通知
      warning(message, options) {
        return showNotification('warning', message, options)
      },
      
      // 显示信息通知
      info(message, options) {
        return showNotification('info', message, options)
      },
      
      // 关闭指定通知
      close: closeNotification,
      
      // 关闭所有通知
      closeAll: closeAllNotifications,
      
      // 获取通知列表
      getNotifications: () => notifications.value
    }
    
    // 提供通知API给所有组件
    app.provide(NOTIFICATION_KEY, notificationMethods)
    
    // 注册全局属性
    app.config.globalProperties.$notify = notificationMethods
    
    console.log('Notification Plugin installed successfully')
  }
}

// Composition API 钩子
function useNotification() {
  const notificationApi = inject(NOTIFICATION_KEY)
  if (!notificationApi) {
    throw new Error('NotificationApi not found, please install NotificationPlugin first')
  }
  return notificationApi
}

export { useNotification }
export default NotificationPlugin