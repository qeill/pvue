import { inject, provide } from 'vue'
import pluginManager from './plugin-manager'

// 注入键
const PLUGIN_MANAGER_KEY = Symbol('plugin-manager')

// 插件系统主入口
const PvuePluginSystem = {
  name: 'pvue-plugin-system',
  
  // 安装方法，支持 app.use()
  install(app, options = {}) {
    // 初始化插件管理器
    pluginManager.init(app)
    
    // 提供插件管理器给所有组件
    app.provide(PLUGIN_MANAGER_KEY, pluginManager)
    
    // 注册全局属性
    app.config.globalProperties.$plugins = pluginManager
    
    // 注册全局方法
    app.config.globalProperties.$registerPlugin = (plugin, pluginOptions) => {
      return pluginManager.register(plugin, pluginOptions)
    }
    
    app.config.globalProperties.$getPlugin = (name) => {
      return pluginManager.get(name)
    }
    
    console.log('Pvue Plugin System installed successfully')
  }
}

// Composition API 钩子：获取插件管理器
function usePluginManager() {
  const manager = inject(PLUGIN_MANAGER_KEY)
  if (!manager) {
    throw new Error('PluginManager not found, please install PvuePluginSystem first')
  }
  return manager
}

// Composition API 钩子：使用特定插件
function usePlugin(name) {
  const manager = usePluginManager()
  const pluginEntry = manager.get(name)
  
  if (!pluginEntry) {
    throw new Error(`Plugin "${name}" not found`)
  }
  
  if (!pluginEntry.enabled) {
    console.warn(`Plugin "${name}" is disabled`)
  }
  
  return {
    plugin: pluginEntry.plugin,
    options: pluginEntry.options,
    enabled: pluginEntry.enabled,
    isEnabled: () => manager.isEnabled(name),
    enable: () => manager.enable(name),
    disable: () => manager.disable(name)
  }
}

// 导出插件系统和钩子
export {
  PvuePluginSystem,
  usePluginManager,
  usePlugin,
  pluginManager // 导出单例，方便直接使用
}

export default PvuePluginSystem