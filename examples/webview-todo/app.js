// Pvue WebView Todo App Vue 应用
const { createApp, ref, computed, onMounted } = Vue;

createApp({
  setup() {
    // 状态管理
    const todos = ref([]);
    const newTodo = ref('');
    const appInfo = ref(null);
    
    // 计算属性：已完成的待办事项数量
    const completedCount = computed(() => {
      return todos.value.filter(todo => todo.completed).length;
    });
    
    // 检查是否在 PyWebView 环境中
    const isWebView = ref(!!window.pywebview);
    
    // 从后端获取待办事项列表
    const fetchTodos = async () => {
      try {
        if (isWebView.value) {
          // PyWebView 环境：使用 window.pywebview.api 调用 Python 函数
          const result = await window.pywebview.api.get_todos();
          todos.value = result;
        } else {
          // 浏览器环境：使用模拟数据
          todos.value = [
            { id: 1, text: '学习 Vue 3', completed: false },
            { id: 2, text: '学习 Python', completed: true },
            { id: 3, text: '开发 Pvue 应用', completed: false }
          ];
        }
      } catch (error) {
        console.error('获取待办事项失败:', error);
      }
    };
    
    // 添加新的待办事项
    const addTodo = async () => {
      if (newTodo.value.trim()) {
        try {
          if (isWebView.value) {
            // PyWebView 环境：使用 window.pywebview.api 调用 Python 函数
            const result = await window.pywebview.api.add_todo(newTodo.value);
            todos.value = result;
            newTodo.value = '';
          } else {
            // 浏览器环境：使用模拟数据
            const newId = Math.max(...todos.value.map(todo => todo.id), 0) + 1;
            todos.value.push({
              id: newId,
              text: newTodo.value,
              completed: false
            });
            newTodo.value = '';
          }
        } catch (error) {
          console.error('添加待办事项失败:', error);
        }
      }
    };
    
    // 更新待办事项
    const updateTodo = async (todo) => {
      try {
        if (isWebView.value) {
          // PyWebView 环境：使用 window.pywebview.api 调用 Python 函数
          const result = await window.pywebview.api.update_todo(todo.id, todo.completed);
          todos.value = result;
        }
        // 浏览器环境：直接更新本地数据
      } catch (error) {
        console.error('更新待办事项失败:', error);
      }
    };
    
    // 删除待办事项
    const deleteTodo = async (id) => {
      try {
        if (isWebView.value) {
          // PyWebView 环境：使用 window.pywebview.api 调用 Python 函数
          const result = await window.pywebview.api.delete_todo(id);
          todos.value = result;
        } else {
          // 浏览器环境：使用本地数据
          todos.value = todos.value.filter(todo => todo.id !== id);
        }
      } catch (error) {
        console.error('删除待办事项失败:', error);
      }
    };
    
    // 清除已完成的待办事项
    const clearCompleted = async () => {
      try {
        if (isWebView.value) {
          // PyWebView 环境：使用 window.pywebview.api 调用 Python 函数
          const result = await window.pywebview.api.clear_completed_todos();
          todos.value = result;
        } else {
          // 浏览器环境：使用本地数据
          todos.value = todos.value.filter(todo => !todo.completed);
        }
      } catch (error) {
        console.error('清除已完成待办事项失败:', error);
      }
    };
    
    // 获取应用信息
    const getAppInfo = async () => {
      try {
        if (isWebView.value) {
          // PyWebView 环境：使用 window.pywebview.api 调用 Python 函数
          const result = await window.pywebview.api.get_app_info();
          appInfo.value = JSON.stringify(result, null, 2);
        } else {
          // 浏览器环境：使用模拟数据
          appInfo.value = JSON.stringify({
            name: 'Pvue WebView Todo App',
            version: '1.0.0',
            mode: 'browser',
            todo_count: todos.value.length,
            completed_count: completedCount.value
          }, null, 2);
        }
      } catch (error) {
        console.error('获取应用信息失败:', error);
      }
    };
    
    // 初始化：获取待办事项列表
    onMounted(() => {
      fetchTodos();
    });
    
    return {
      todos,
      newTodo,
      appInfo,
      completedCount,
      addTodo,
      updateTodo,
      deleteTodo,
      clearCompleted,
      getAppInfo
    };
  }
}).mount('#app');
