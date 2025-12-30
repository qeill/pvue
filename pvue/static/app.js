// 科学计算器Vue应用
const { createApp, ref } = Vue;

createApp({
  setup() {
    // 状态管理
    const display = ref('0');
    const history = ref('');
    let currentInput = '0';
    let operator = null;
    let previousInput = null;
    let shouldResetDisplay = false;

    // 辅助函数
    const updateDisplay = () => {
      display.value = currentInput;
    };

    // 清除所有
    const clear = () => {
      currentInput = '0';
      previousInput = null;
      operator = null;
      history.value = '';
      updateDisplay();
    };

    // 清除当前输入
    const clearEntry = () => {
      currentInput = '0';
      updateDisplay();
    };

    // 删除最后一个字符
    const backspace = () => {
      if (currentInput.length > 1) {
        currentInput = currentInput.slice(0, -1);
      } else {
        currentInput = '0';
      }
      updateDisplay();
    };

    // 切换正负号
    const toggleSign = () => {
      if (currentInput !== '0') {
        currentInput = currentInput.startsWith('-') 
          ? currentInput.slice(1) 
          : '-' + currentInput;
        updateDisplay();
      }
    };

    // 百分比转换
    const percentage = () => {
      const num = parseFloat(currentInput);
      currentInput = (num / 100).toString();
      updateDisplay();
    };

    // 添加数字或小数点
    const append = (value) => {
      if (shouldResetDisplay) {
        currentInput = '0';
        shouldResetDisplay = false;
      }

      if (value === '.' && currentInput.includes('.')) {
        return;
      }

      if (currentInput === '0' && value !== '.') {
        currentInput = value;
      } else {
        currentInput += value;
      }
      updateDisplay();
    };

    // 设置运算符
    const setOperator = (op) => {
      if (operator !== null) {
        equals();
      }
      previousInput = currentInput;
      operator = op;
      history.value = `${previousInput} ${op}`;
      shouldResetDisplay = true;
    };

    // 阶乘计算
    const factorial = (n) => {
      if (n < 0) return NaN;
      if (n === 0 || n === 1) return 1;
      let result = 1;
      for (let i = 2; i <= n; i++) {
        result *= i;
      }
      return result;
    };

    // 科学计算
    const calculate = (func) => {
      const num = parseFloat(currentInput);
      let result;

      try {
        switch (func) {
          case 'sin':
            result = Math.sin(num * Math.PI / 180);
            break;
          case 'cos':
            result = Math.cos(num * Math.PI / 180);
            break;
          case 'tan':
            result = Math.tan(num * Math.PI / 180);
            break;
          case 'asin':
            result = Math.asin(num) * 180 / Math.PI;
            break;
          case 'acos':
            result = Math.acos(num) * 180 / Math.PI;
            break;
          case 'atan':
            result = Math.atan(num) * 180 / Math.PI;
            break;
          case 'log':
            result = Math.log(num);
            break;
          case 'ln':
            result = Math.log10(num);
            break;
          case 'log10':
            result = Math.log10(num);
            break;
          case 'sqrt':
            result = Math.sqrt(num);
            break;
          case 'pow':
            result = Math.pow(num, 2);
            break;
          case 'pow3':
            result = Math.pow(num, 3);
            break;
          case '1/x':
            result = 1 / num;
            break;
          case 'pi':
            result = Math.PI;
            break;
          case 'e':
            result = Math.E;
            break;
          case '!':
            result = factorial(num);
            break;
          case '(': 
            append('(');
            return;
          case ')':
            append(')');
            return;
          default:
            result = num;
        }

        // 处理结果
        result = parseFloat(result.toFixed(12));
        currentInput = result.toString();
        history.value = `${func}(${display.value})`;
        updateDisplay();
      } catch (error) {
        currentInput = 'Error';
        updateDisplay();
      }
    };

    // 等号计算
    const equals = () => {
      if (operator === null) return;

      try {
        // 构建表达式
        let expression = `${previousInput} ${operator} ${currentInput}`;
        history.value = expression;

        // 替换运算符为JavaScript运算符
        expression = expression
          .replace(/×/g, '*')
          .replace(/÷/g, '/')
          .replace(/^/g, '**');

        // 计算结果
        const result = eval(expression);
        currentInput = parseFloat(result.toFixed(12)).toString();
        updateDisplay();

        // 重置状态
        operator = null;
        previousInput = null;
        shouldResetDisplay = true;
      } catch (error) {
        currentInput = 'Error';
        updateDisplay();
        operator = null;
        previousInput = null;
      }
    };

    return {
      display,
      history,
      clear,
      clearEntry,
      backspace,
      toggleSign,
      percentage,
      append,
      setOperator,
      calculate,
      equals
    };
  }
}).mount('#app');