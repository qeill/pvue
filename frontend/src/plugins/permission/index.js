import { inject, provide, ref } from 'vue'

// 注入键
const PERMISSION_KEY = Symbol('permission')

// 权限控制插件
const PermissionPlugin = {
  name: 'permission',
  
  // 安装方法
  install(app, options = {}) {
    // 初始化权限数据
    const permissions = ref(options.initialPermissions || [])
    const roles = ref(options.initialRoles || [])
    
    // 权限检查函数
    const checkPermission = (permission) => {
      if (!permission) return true
      return permissions.value.includes(permission)
    }
    
    // 角色检查函数
    const checkRole = (role) => {
      if (!role) return true
      return roles.value.includes(role)
    }
    
    // 多权限检查（AND）
    const checkAllPermissions = (...permissionList) => {
      return permissionList.every(checkPermission)
    }
    
    // 多权限检查（OR）
    const checkAnyPermission = (...permissionList) => {
      return permissionList.some(checkPermission)
    }
    
    // 多角色检查（AND）
    const checkAllRoles = (...roleList) => {
      return roleList.every(checkRole)
    }
    
    // 多角色检查（OR）
    const checkAnyRole = (...roleList) => {
      return roleList.some(checkRole)
    }
    
    // 更新权限
    const updatePermissions = (newPermissions) => {
      permissions.value = newPermissions
    }
    
    // 更新角色
    const updateRoles = (newRoles) => {
      roles.value = newRoles
    }
    
    // 添加权限
    const addPermission = (permission) => {
      if (!permissions.value.includes(permission)) {
        permissions.value.push(permission)
      }
    }
    
    // 移除权限
    const removePermission = (permission) => {
      const index = permissions.value.indexOf(permission)
      if (index > -1) {
        permissions.value.splice(index, 1)
      }
    }
    
    // 添加角色
    const addRole = (role) => {
      if (!roles.value.includes(role)) {
        roles.value.push(role)
      }
    }
    
    // 移除角色
    const removeRole = (role) => {
      const index = roles.value.indexOf(role)
      if (index > -1) {
        roles.value.splice(index, 1)
      }
    }
    
    // 权限API对象
    const permissionApi = {
      // 数据
      permissions,
      roles,
      
      // 检查方法
      check: checkPermission,
      checkRole,
      checkAll: checkAllPermissions,
      checkAny: checkAnyPermission,
      checkAllRoles,
      checkAnyRole,
      
      // 更新方法
      updatePermissions,
      updateRoles,
      addPermission,
      removePermission,
      addRole,
      removeRole
    }
    
    // 提供权限API给所有组件
    app.provide(PERMISSION_KEY, permissionApi)
    
    // 注册全局属性
    app.config.globalProperties.$permission = permissionApi
    
    // 注册自定义指令：v-permission
    app.directive('permission', {
      mounted(el, binding) {
        const hasPermission = checkPermission(binding.value)
        if (!hasPermission) {
          el.style.display = 'none'
        }
      },
      
      updated(el, binding) {
        const hasPermission = checkPermission(binding.value)
        if (hasPermission) {
          el.style.display = ''
        } else {
          el.style.display = 'none'
        }
      }
    })
    
    // 注册自定义指令：v-role
    app.directive('role', {
      mounted(el, binding) {
        const hasRole = checkRole(binding.value)
        if (!hasRole) {
          el.style.display = 'none'
        }
      },
      
      updated(el, binding) {
        const hasRole = checkRole(binding.value)
        if (hasRole) {
          el.style.display = ''
        } else {
          el.style.display = 'none'
        }
      }
    })
    
    console.log('Permission Plugin installed successfully')
  }
}

// Composition API 钩子
function usePermission() {
  const permissionApi = inject(PERMISSION_KEY)
  if (!permissionApi) {
    throw new Error('PermissionApi not found, please install PermissionPlugin first')
  }
  return permissionApi
}

export { usePermission }
export default PermissionPlugin