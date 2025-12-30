# Pvue 插件系统开发文档

## 1. 概述

Pvue 插件系统提供了一个灵活的扩展机制，允许开发者通过简单的注册方式添加自定义功能，如权限控制、消息通知等。插件系统支持 Vue 3 的 Composition API，可通过 `app.use()` 方法全局注册，也能在组件内按需使用。

## 2. 核心特性

- ✅ 支持 `app.use()` 全局注册
- ✅ 支持 Composition API 按需使用
- ✅ 提供插件管理器，统一管理所有插件
- ✅ 支持插件启用/禁用
- ✅ 提供完整的 TypeScript 支持
- ✅ 易于扩展和定制

## 3. 快速开始

### 3.1 安装插件系统

在 `main.js` 中注册插件系统：

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import { PvuePluginSystem } from './plugins'

const app = createApp(App)

// 注册插件系统
app.use(PvuePluginSystem)

app.mount('#app')
```

### 3.2 注册自定义插件

```javascript
// 导入插件
import PermissionPlugin from './plugins/permission'
import NotificationPlugin from './plugins/notification'

// 注册插件
app.use(PermissionPlugin, {
  initialPermissions: ['read', 'write'],
  initialRoles: ['user']
})

app.use(NotificationPlugin, {
  duration: 5000,
  position: 'top-right'
})
```

## 4. 插件开发指南

### 4.1 插件结构

一个标准的 Pvue 插件应包含以下结构：

```javascript
const MyPlugin = {
  name: 'my-plugin',
  
  // 安装方法
  install(app, options = {}) {
    // 插件初始化逻辑
    
    // 注册全局属性
    app.config.globalProperties.$myPlugin = {
      // 插件方法
    }
    
    // 提供 Composition API 支持
    app.provide(MY_PLUGIN_KEY, pluginApi)
    
    // 注册自定义指令
    app.directive('my-directive', directiveOptions)
    
    // 注册组件
    app.component('MyComponent', MyComponent)
  }
}

export default MyPlugin
```

### 4.2 插件API设计

一个好的插件应该提供：

1. **全局属性**：通过 `app.config.globalProperties` 注册，支持选项API
2. **Composition API 钩子**：通过 `app.provide` 提供，支持组合式API
3. **自定义指令**：方便在模板中使用
4. **组件**：提供UI组件支持

### 4.3 插件开发示例

```javascript
import { inject, provide, ref } from 'vue'

// 注入键
const MY_PLUGIN_KEY = Symbol('my-plugin')

const MyPlugin = {
  name: 'my-plugin',
  
  install(app, options = {}) {
    // 插件状态
    const state = ref(options.initialValue || '')
    
    // 插件方法
    const setValue = (value) => {
      state.value = value
    }
    
    const getValue = () => {
      return state.value
    }
    
    // API对象
    const pluginApi = {
      state,
      setValue,
      getValue
    }
    
    // 提供给Composition API
    app.provide(MY_PLUGIN_KEY, pluginApi)
    
    // 注册全局属性
    app.config.globalProperties.$myPlugin = pluginApi
    
    console.log('MyPlugin installed successfully')
  }
}

// Composition API钩子
function useMyPlugin() {
  const api = inject(MY_PLUGIN_KEY)
  if (!api) {
    throw new Error('MyPlugin not found, please install it first')
  }
  return api
}

export { useMyPlugin }
export default MyPlugin
```

## 5. 内置插件使用

### 5.1 权限控制插件 (PermissionPlugin)

#### 5.1.1 安装

```javascript
import PermissionPlugin from './plugins/permission'

app.use(PermissionPlugin, {
  initialPermissions: ['read', 'write'], // 初始权限
  initialRoles: ['user'] // 初始角色
})
```

#### 5.1.2 Composition API 使用

```vue
<template>
  <div>
    <button v-permission="'write'">只有写权限可见</button>
    <button v-role="'admin'">只有管理员可见</button>
    
    <div v-if="canWrite">
      <textarea v-model="content"></textarea>
      <button @click="save">保存</button>
    </div>
  </div>
</template>

<script setup>
import { usePermission } from './plugins/permission'

const { check, checkRole, addPermission, removePermission } = usePermission()
const canWrite = check('write')
const isAdmin = checkRole('admin')

const content = ref('')

const save = () => {
  if (canWrite) {
    // 保存逻辑
  }
}

// 添加权限
const grantPermission = () => {
  addPermission('delete')
}

// 移除权限
const revokePermission = () => {
  removePermission('write')
}
</script>
```

#### 5.1.3 API 参考

| 方法 | 描述 | 参数 | 返回值 |
|------|------|------|--------|
| `check(permission)` | 检查单个权限 | `permission: string` | `boolean` |
| `checkRole(role)` | 检查单个角色 | `role: string` | `boolean` |
| `checkAll(...permissions)` | 检查所有权限（AND） | `permissions: string[]` | `boolean` |
| `checkAny(...permissions)` | 检查任一权限（OR） | `permissions: string[]` | `boolean` |
| `checkAllRoles(...roles)` | 检查所有角色（AND） | `roles: string[]` | `boolean` |
| `checkAnyRole(...roles)` | 检查任一角色（OR） | `roles: string[]` | `boolean` |
| `updatePermissions(permissions)` | 更新权限列表 | `permissions: string[]` | `void` |
| `updateRoles(roles)` | 更新角色列表 | `roles: string[]` | `void` |
| `addPermission(permission)` | 添加单个权限 | `permission: string` | `void` |
| `removePermission(permission)` | 移除单个权限 | `permission: string` | `void` |
| `addRole(role)` | 添加单个角色 | `role: string` | `void` |
| `removeRole(role)` | 移除单个角色 | `role: string` | `void` |

#### 5.1.4 自定义指令

- **`v-permission`**：根据权限控制元素显示/隐藏
- **`v-role`**：根据角色控制元素显示/隐藏

### 5.2 消息通知插件 (NotificationPlugin)

#### 5.2.1 安装

```javascript
import NotificationPlugin from './plugins/notification'

app.use(NotificationPlugin, {
  duration: 3000, // 自动关闭时间（毫秒）
  position: 'top-right', // 显示位置
  closeable: true // 是否可关闭
})
```

#### 5.2.2 Composition API 使用

```vue
<template>
  <div>
    <button @click="showSuccess">成功通知</button>
    <button @click="showError">错误通知</button>
    <button @click="showWarning">警告通知</button>
    <button @click="showInfo">信息通知</button>
  </div>
</template>

<script setup>
import { useNotification } from './plugins/notification'

const notify = useNotification()

const showSuccess = () => {
  notify.success('操作成功', {
    title: '成功',
    duration: 2000
  })
}

const showError = () => {
  notify.error('操作失败，请重试', {
    title: '错误',
    duration: 5000
  })
}

const showWarning = () => {
  notify.warning('请注意，这是一个警告', {
    position: 'top-left'
  })
}

const showInfo = () => {
  notify.info('这是一条提示信息', {
    closeable: false
  })
}
</script>
```

#### 5.2.3 API 参考

| 方法 | 描述 | 参数 | 返回值 |
|------|------|------|--------|
| `success(message, options)` | 显示成功通知 | `message: string`<br>`options: object` | `string` (通知ID) |
| `error(message, options)` | 显示错误通知 | `message: string`<br>`options: object` | `string` (通知ID) |
| `warning(message, options)` | 显示警告通知 | `message: string`<br>`options: object` | `string` (通知ID) |
| `info(message, options)` | 显示信息通知 | `message: string`<br>`options: object` | `string` (通知ID) |
| `close(id)` | 关闭指定通知 | `id: string` | `void` |
| `closeAll()` | 关闭所有通知 | - | `void` |
| `getNotifications()` | 获取所有通知 | - | `array` |

#### 5.2.4 通知选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `title` | `string` | `undefined` | 通知标题 |
| `duration` | `number` | `3000` | 自动关闭时间（毫秒） |
| `position` | `string` | `top-right` | 显示位置（top-right, top-left, bottom-right, bottom-left） |
| `closeable` | `boolean` | `true` | 是否显示关闭按钮 |

## 6. 插件管理器

### 6.1 访问插件管理器

```javascript
// 通过全局属性访问
app.config.globalProperties.$plugins

// 通过 Composition API 访问
import { usePluginManager } from './plugins'
const pluginManager = usePluginManager()
```

### 6.2 插件管理器 API

| 方法 | 描述 | 参数 | 返回值 |
|------|------|------|--------|
| `register(plugin, options)` | 注册插件 | `plugin: object`<br>`options: object` | `PluginManager` (链式调用) |
| `get(name)` | 获取插件 | `name: string` | `PluginEntry` |
| `has(name)` | 检查插件是否存在 | `name: string` | `boolean` |
| `getAll()` | 获取所有插件 | - | `array` |
| `enable(name)` | 启用插件 | `name: string` | `PluginManager` |
| `disable(name)` | 禁用插件 | `name: string` | `PluginManager` |
| `isEnabled(name)` | 检查插件是否启用 | `name: string` | `boolean` |

## 7. 最佳实践

### 7.1 插件命名规范

- 插件名称应具有描述性，使用小写字母，单词间用连字符分隔
- 插件文件应放在 `src/plugins/` 目录下
- 每个插件应有独立的目录，包含核心代码和样式文件

### 7.2 插件设计原则

- **单一职责**：每个插件应只负责一个功能领域
- **可配置性**：提供合理的默认配置和自定义选项
- **向后兼容**：确保插件升级时不会破坏现有功能
- **文档完善**：提供清晰的使用说明和API参考
- **错误处理**：完善的错误处理和异常捕获

### 7.3 性能考虑

- 避免在插件初始化时执行耗时操作
- 合理使用缓存，避免重复计算
- 插件应支持按需加载
- 考虑使用虚拟列表等技术优化大量数据渲染

## 8. 示例插件开发流程

### 8.1 创建插件目录

```bash
mkdir -p src/plugins/my-plugin
```

### 8.2 编写插件核心代码

```javascript
// src/plugins/my-plugin/index.js
import { inject, provide, ref } from 'vue'
import './style.css'

const MY_PLUGIN_KEY = Symbol('my-plugin')

const MyPlugin = {
  name: 'my-plugin',
  
  install(app, options = {}) {
    // 插件逻辑
    const count = ref(0)
    
    const increment = () => {
      count.value++
    }
    
    const decrement = () => {
      count.value--
    }
    
    const pluginApi = {
      count,
      increment,
      decrement
    }
    
    // 提供给组件
    app.provide(MY_PLUGIN_KEY, pluginApi)
    app.config.globalProperties.$myPlugin = pluginApi
    
    console.log('MyPlugin installed')
  }
}

function useMyPlugin() {
  const api = inject(MY_PLUGIN_KEY)
  if (!api) {
    throw new Error('MyPlugin not found')
  }
  return api
}

export { useMyPlugin }
export default MyPlugin
```

### 8.3 编写样式文件

```css
/* src/plugins/my-plugin/style.css */
.my-plugin {
  /* 样式 */
}
```

### 8.4 注册和使用插件

```javascript
// main.js
import MyPlugin from './plugins/my-plugin'
app.use(MyPlugin)

// 组件中使用
<template>
  <div>
    <div>{{ count }}</div>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
  </div>
</template>

<script setup>
import { useMyPlugin } from './plugins/my-plugin'
const { count, increment, decrement } = useMyPlugin()
</script>
```

## 9. 故障排除

### 9.1 常见问题

1. **插件未找到**
   - 确保插件已正确注册
   - 检查插件名称是否正确
   - 确保插件系统已先于其他插件注册

2. **Composition API 钩子报错**
   - 确保插件已安装
   - 检查注入键是否正确
   - 确保在组件的 `setup()` 函数中使用

3. **插件冲突**
   - 避免使用相同的插件名称
   - 避免使用相同的全局属性名
   - 使用唯一的注入键

## 10. 未来规划

- [ ] 支持插件热重载
- [ ] 提供插件市场
- [ ] 支持插件依赖管理
- [ ] 提供更完善的 TypeScript 类型定义
- [ ] 支持插件配置可视化管理

## 11. 贡献

欢迎贡献插件系统的改进和新插件的开发！请遵循以下准则：

1. 提交 PR 前确保所有测试通过
2. 提供清晰的文档和示例
3. 遵循现有的代码风格
4. 确保向后兼容

## 12. 许可证

MIT License

---

**Pvue 插件系统** - 让扩展变得简单！