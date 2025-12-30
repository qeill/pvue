import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

// 导入插件系统和示例插件
import { PvuePluginSystem } from './plugins'
import PermissionPlugin from './plugins/permission'
import NotificationPlugin from './plugins/notification'

const app = createApp(App)

// 注册插件系统
app.use(PvuePluginSystem)

// 注册权限控制插件
app.use(PermissionPlugin, {
  initialPermissions: ['read', 'write'],
  initialRoles: ['user']
})

// 注册消息通知插件
app.use(NotificationPlugin, {
  duration: 3000,
  position: 'top-right'
})

app.mount('#app')