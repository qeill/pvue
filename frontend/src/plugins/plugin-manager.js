// 插件管理器核心类
class PluginManager {
  constructor() {
    this.plugins = new Map() // 存储注册的插件
    this.app = null // Vue应用实例
    this.context = null // 插件上下文
  }

  // 初始化插件管理器
  init(app) {
    this.app = app
    this.context = {
      app,
      config: app.config,
      globalProperties: app.config.globalProperties
    }
  }

  // 注册插件
  register(plugin, options = {}) {
    const { name } = plugin
    
    if (!name) {
      throw new Error('Plugin must have a name property')
    }

    if (this.plugins.has(name)) {
      console.warn(`Plugin "${name}" has already been registered`)
      return this
    }

    try {
      // 调用插件的install方法
      if (typeof plugin.install === 'function') {
        plugin.install(this.context, options)
      }
      
      // 存储插件实例和配置
      this.plugins.set(name, {
        plugin,
        options,
        enabled: true
      })
      
      console.log(`Plugin "${name}" registered successfully`)
    } catch (error) {
      console.error(`Failed to register plugin "${name}":`, error)
      throw error
    }

    return this
  }

  // 获取插件
  get(name) {
    return this.plugins.get(name)
  }

  // 检查插件是否已注册
  has(name) {
    return this.plugins.has(name)
  }

  // 获取所有插件
  getAll() {
    return Array.from(this.plugins.values())
  }

  // 启用插件
  enable(name) {
    const pluginEntry = this.plugins.get(name)
    if (pluginEntry) {
      pluginEntry.enabled = true
      console.log(`Plugin "${name}" enabled`)
    }
    return this
  }

  // 禁用插件
  disable(name) {
    const pluginEntry = this.plugins.get(name)
    if (pluginEntry) {
      pluginEntry.enabled = false
      console.log(`Plugin "${name}" disabled`)
    }
    return this
  }

  // 检查插件是否启用
  isEnabled(name) {
    const pluginEntry = this.plugins.get(name)
    return pluginEntry ? pluginEntry.enabled : false
  }
}

// 创建并导出单例实例
const pluginManager = new PluginManager()
export default pluginManager