// Pvue Eel Todo App Vue 应用
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
    
    // 从后端获取待办事项列表
    const fetchTodos = async () => {
      try {
        const result = await eel.get_todos()();
        todos.value = result;
      } catch (error) {
        console.error('获取待办事项失败:', error);
      }
    };
    
    // 添加新的待办事项
    const addTodo = async () => {
      if (newTodo.value.trim()) {
        try {
          const result = await eel.add_todo(newTodo.value)();
          todos.value = result;
          newTodo.value = '';
        } catch (error) {
          console.error('添加待办事项失败:', error);
        }
      }
    };
    
    // 更新待办事项
    const updateTodo = async (todo) => {
      try {
        const result = await eel.update_todo(todo.id, todo.completed)();
        todos.value = result;
      } catch (error) {
        console.error('更新待办事项失败:', error);
      }
    };
    
    // 删除待办事项
    const deleteTodo = async (id) => {
      try {
        const result = await eel.delete_todo(id)();
        todos.value = result;
      } catch (error) {
        console.error('删除待办事项失败:', error);
      }
    };
    
    // 清除已完成的待办事项
    const clearCompleted = async () => {
      try {
        const result = await eel.clear_completed_todos()();
        todos.value = result;
      } catch (error) {
        console.error('清除已完成待办事项失败:', error);
      }
    };
    
    // 获取应用信息
    const getAppInfo = async () => {
      try {
        const result = await eel.get_app_info()();
        appInfo.value = JSON.stringify(result, null, 2);
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
