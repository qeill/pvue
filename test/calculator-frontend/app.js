// Pvue 科学计算器 Vue 应用
const { createApp, ref, computed, onMounted, onBeforeUnmount } = Vue;

createApp({
  setup() {
    // WebSocket连接配置
    const wsUrl = 'ws://localhost:9001';
    let ws = null;
    let isConnecting = false;
    let reconnectTimer = null;
    
    // 状态管理
    const display = ref('');
    const history = ref('');
    const isScientific = ref(false);
    const message = ref(null);
    const pendingOperation = ref(null);
    const previousValue = ref(0);
    
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
          showMessage('计算器已连接到服务器', 'success');
        };
        
        // 连接关闭事件
        ws.onclose = () => {
          console.log('WebSocket连接已关闭');
          isConnecting = false;
          showMessage('计算器与服务器连接已断开', 'error');
          // 3秒后尝试重连
          reconnectTimer = setTimeout(() => {
            connectWebSocket();
          }, 3000);
        };
        
        // 连接错误事件
        ws.onerror = (error) => {
          console.error('WebSocket连接错误:', error);
          isConnecting = false;
          showMessage('计算器连接到服务器失败', 'error');
        };
        
      } catch (error) {
        console.error('WebSocket连接失败:', error);
        isConnecting = false;
        showMessage(`连接失败：${error.message}`, 'error');
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
            resolve(response.result);
          } catch (error) {
            ws.removeEventListener('message', handleResponse);
            reject(new Error('响应解析失败'));
          }
        };
        
        // 添加临时事件处理器
        ws.addEventListener('message', handleResponse);
      });
    };
    
    // 切换标准/科学模式
    const toggleMode = () => {
      isScientific.value = !isScientific.value;
      showMessage(`已切换到${isScientific.value ? '科学' : '标准'}模式`, 'info');
    };
    
    // 清除显示屏
    const clear = () => {
      display.value = '';
      history.value = '';
      pendingOperation.value = null;
      previousValue.value = 0;
    };
    
    // 清除当前输入
    const clearEntry = () => {
      display.value = '';
    };
    
    // 退格
    const backspace = () => {
      if (display.value.length > 0) {
        display.value = display.value.slice(0, -1);
      }
    };
    
    // 追加数字
    const appendNumber = (number) => {
      display.value += number;
    };
    
    // 追加小数点
    const appendDecimal = () => {
      if (!display.value.includes('.')) {
        display.value += '.';
      }
    };
    
    // 追加运算符
    const appendOperator = (operator) => {
      if (display.value === '') return;
      
      if (pendingOperation.value) {
        calculate();
      }
      
      history.value = `${display.value} ${operator}`;
      previousValue.value = parseFloat(display.value);
      pendingOperation.value = operator;
      display.value = '';
    };
    
    // 追加函数
    const appendFunction = (func) => {
      display.value += func;
    };
    
    // 切换正负号
    const toggleSign = () => {
      if (display.value === '') return;
      
      if (display.value.startsWith('-')) {
        display.value = display.value.slice(1);
      } else {
        display.value = '-' + display.value;
      }
    };
    
    // 执行计算
    const calculate = async () => {
      if (!display.value) return;
      
      let expression = '';
      
      if (pendingOperation.value) {
        // 处理标准运算
        expression = `${previousValue.value} ${pendingOperation.value} ${display.value}`;
      } else {
        // 处理表达式运算
        expression = display.value;
      }
      
      try {
        // 调用后端计算函数
        const result = await sendMessage('calculate', [expression]);
        
        if (result.success) {
          history.value = `${expression} =`;
          display.value = result.result.toString();
          pendingOperation.value = null;
        } else {
          showMessage(`计算错误：${result.error}`, 'error');
        }
      } catch (error) {
        showMessage(`计算失败：${error.message}`, 'error');
        console.error('计算失败:', error);
      }
    };
    
    // 初始化：连接WebSocket
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
      display,
      history,
      isScientific,
      message,
      toggleMode,
      clear,
      clearEntry,
      backspace,
      appendNumber,
      appendDecimal,
      appendOperator,
      appendFunction,
      toggleSign,
      calculate
    };
  }
}).mount('#app');