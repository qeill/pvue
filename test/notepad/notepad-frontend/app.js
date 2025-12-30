// Pvue 记事本 Vue 应用
const { createApp, ref, computed, onMounted, onBeforeUnmount } = Vue;

createApp({
  setup() {
    // WebSocket连接配置
    const wsUrl = 'ws://localhost:9000';
    let ws = null;
    let isConnecting = false;
    let reconnectTimer = null;
    
    // 状态管理
    const notes = ref([]);
    const selectedNote = ref(null);
    const searchQuery = ref('');
    const message = ref(null);
    
    // 备份当前编辑的笔记，用于取消编辑
    const backupNote = ref(null);
    
    // 计算属性：过滤后的笔记列表
    const filteredNotes = computed(() => {
      if (!searchQuery.value) {
        return notes.value;
      }
      const query = searchQuery.value.toLowerCase();
      return notes.value.filter(note => 
        note.title.toLowerCase().includes(query) || 
        note.content.toLowerCase().includes(query)
      );
    });
    
    // 显示消息提示
    const showMessage = (text, type = 'info') => {
      message.value = { text, type };
      // 3秒后自动隐藏消息
      setTimeout(() => {
        message.value = null;
      }, 3000);
    };
    
    // 连接WebSocket
    const connectWebSocket = () => {
      if (isConnecting || (ws && ws.readyState === WebSocket.OPEN)) {
        return;
      }
      
      isConnecting = true;
      
      try {
        ws = new WebSocket(wsUrl);
        
        // 连接打开事件
        ws.onopen = () => {
          console.log('WebSocket连接已建立');
          isConnecting = false;
          fetchNotes();
        };
        
        // 连接关闭事件
        ws.onclose = () => {
          console.log('WebSocket连接已关闭');
          isConnecting = false;
          // 3秒后尝试重连
          reconnectTimer = setTimeout(() => {
            connectWebSocket();
          }, 3000);
        };
        
        // 连接错误事件
        ws.onerror = (error) => {
          console.error('WebSocket连接错误:', error);
          isConnecting = false;
        };
        
      } catch (error) {
        console.error('WebSocket连接失败:', error);
        isConnecting = false;
        // 3秒后尝试重连
        reconnectTimer = setTimeout(() => {
          connectWebSocket();
        }, 3000);
      }
    };
    
    // 发送消息到后端
    const sendMessage = (functionName, params = []) => {
      return new Promise((resolve, reject) => {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
          reject(new Error('WebSocket连接未建立'));
          return;
        }
        
        // 创建请求对象
        const request = {
          function: functionName,
          params: params
        };
        
        // 发送请求
        ws.send(JSON.stringify(request));
        
        // 临时事件处理器，用于接收特定请求的响应
        const handleResponse = (event) => {
          try {
            const response = JSON.parse(event.data);
            // 移除临时事件处理器
            ws.removeEventListener('message', handleResponse);
            resolve(response);
          } catch (error) {
            ws.removeEventListener('message', handleResponse);
            reject(new Error('响应解析失败'));
          }
        };
        
        // 添加临时事件处理器
        ws.addEventListener('message', handleResponse);
      });
    };
    
    // 获取所有笔记
    const fetchNotes = async () => {
      try {
        const response = await sendMessage('get_notes');
        notes.value = response.result;
        showMessage('笔记加载成功', 'success');
      } catch (error) {
        showMessage(`获取笔记失败：${error.message}`, 'error');
      }
    };
    
    // 选择笔记进行编辑
    const selectNote = (note) => {
      selectedNote.value = { ...note };
      backupNote.value = { ...note };
    };
    
    // 添加新笔记
    const addNewNote = async () => {
      try {
        const title = '新笔记';
        const content = '';
        const response = await sendMessage('add_note', [title, content]);
        const newNote = response.result;
        notes.value.push(newNote);
        selectedNote.value = { ...newNote };
        backupNote.value = { ...newNote };
        showMessage('笔记创建成功', 'success');
      } catch (error) {
        showMessage(`创建笔记失败：${error.message}`, 'error');
      }
    };
    
    // 更新笔记
    const updateNote = async () => {
      if (!selectedNote.value) return;
      
      try {
        const { id, title, content } = selectedNote.value;
        const response = await sendMessage('update_note', [id, title, content]);
        const updatedNote = response.result;
        if (updatedNote) {
          // 更新笔记列表中的对应笔记
          const index = notes.value.findIndex(note => note.id === id);
          if (index !== -1) {
            notes.value[index] = updatedNote;
          }
        }
      } catch (error) {
        showMessage(`更新笔记失败：${error.message}`, 'error');
      }
    };
    
    // 保存当前编辑的笔记
    const saveNote = () => {
      if (!selectedNote.value) return;
      
      updateNote();
      showMessage('笔记保存成功', 'success');
      backupNote.value = { ...selectedNote.value };
    };
    
    // 取消编辑
    const cancelEdit = () => {
      if (!backupNote.value) {
        selectedNote.value = null;
        return;
      }
      
      // 恢复备份的笔记
      const index = notes.value.findIndex(note => note.id === backupNote.value.id);
      if (index !== -1) {
        notes.value[index] = { ...backupNote.value };
      }
      selectedNote.value = { ...backupNote.value };
      showMessage('编辑已取消', 'info');
    };
    
    // 删除笔记
    const deleteNote = async (id) => {
      if (confirm('确定要删除这条笔记吗？')) {
        try {
          await sendMessage('delete_note', [id]);
          // 从本地列表中移除
          notes.value = notes.value.filter(note => note.id !== id);
          if (selectedNote.value && selectedNote.value.id === id) {
            selectedNote.value = null;
            backupNote.value = null;
          }
          showMessage('笔记删除成功', 'success');
        } catch (error) {
          showMessage(`删除笔记失败：${error.message}`, 'error');
        }
      }
    };
    
    // 保存所有笔记到文件
    const saveNotes = async () => {
      try {
        const response = await sendMessage('save_notes');
        const result = response.result;
        if (result.success) {
          showMessage('所有笔记保存成功', 'success');
        } else {
          showMessage(`保存失败：${result.message}`, 'error');
        }
      } catch (error) {
        showMessage(`保存失败：${error.message}`, 'error');
      }
    };
    
    // 从文件加载笔记
    const loadNotes = async () => {
      try {
        const response = await sendMessage('load_notes');
        const result = response.result;
        if (result.success) {
          notes.value = result.notes;
          selectedNote.value = null;
          backupNote.value = null;
          showMessage('笔记加载成功', 'success');
        } else {
          showMessage(`加载失败：${result.message}`, 'error');
        }
      } catch (error) {
        showMessage(`加载失败：${error.message}`, 'error');
      }
    };
    
    // 初始化：连接WebSocket并获取笔记列表
    onMounted(() => {
      connectWebSocket();
    });
    
    // 组件卸载时清理资源
    onBeforeUnmount(() => {
      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
      }
      if (ws) {
        ws.close();
      }
    });
    
    return {
      notes,
      selectedNote,
      searchQuery,
      filteredNotes,
      message,
      fetchNotes,
      selectNote,
      addNewNote,
      updateNote,
      saveNote,
      cancelEdit,
      deleteNote,
      saveNotes,
      loadNotes
    };
  }
}).mount('#app');
