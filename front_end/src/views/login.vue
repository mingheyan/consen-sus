<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

const router = useRouter();
const ruleFormRef = ref<FormInstance | null>(null);

const checkAge = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('请输入账号'));
  }
  setTimeout(() => {
    if (!Number.isInteger(value)) {
      callback(new Error('请输入数字'));
    } else {
      if (value.length < 6 || value.length > 12) {
        callback(new Error('账号长度必须大于6且小于12'));
      } else {
        callback();
      }
    }
  }, 1000);
};

const validatePasswordLength = (rule: any, value: any, callback: any) => {
  if (value.length < 8) {
    callback(new Error('密码长度必须大于等于8位'));
  } else {
    callback();
  }
};

const ruleForm = reactive({
  pass: '',
  account: '',
});

const rules = reactive({
  pass: [
    { validator: validatePasswordLength, trigger: 'blur' }
  ],
  account: [
    { validator: checkAge, trigger: 'blur' }
  ],
});

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  
  try {
    // 验证表单
    const valid = await formEl.validate();
    if (valid) {
      // 表单验证通过，发送请求到后端
      const response = await axios.post('你的后端API地址', {
        account: ruleForm.account,
        pass: ruleForm.pass,
      });
      
      // 处理响应
      if (response.status === 200) {
        console.log('提交成功:', response.data);
        // 这里可以进行一些操作，比如路由跳转
        router.push('/home');
      } else {
        console.error('提交失败:', response.data);
      }
    } else {
      console.log('表单验证失败');
    }
  } catch (error) {
    // 捕获并处理错误
    console.error('提交表单时发生错误:', error);
  }
};

const resetFormAndNavigateToRegister = () => {
  // 跳转到注册界面
  router.push('/register');
};
</script>

<template>
  <div class="login-container">
    <!-- 左侧展示区 -->
    <div class="showcase">
      <div class="showcase-content">
        <h1>欢迎回来</h1>
        <p>登录您的账号以继续使用我们的服务</p>
      </div>
    </div>

    <!-- 右侧登录表单 -->
    <el-form
      ref="ruleFormRef"
      style="max-width: 600px"
      :model="ruleForm"
      status-icon
      :rules="rules"
      label-width="auto"
      class="form-container"
    >
      <div class="login-form">
        <div class="logo">
          <img src="/src/assets/logo.jpg" :fit="fit" alt="logo">
        </div>

        <h2>登录</h2>
        <p class="subtitle">请输入您的账号信息</p>

        <el-form-item label="账号" prop="account" class="form-group">
          <div class="input-wrapper">
            <el-input v-model="ruleForm.account" placeholder="请输入用户名" />
          </div>
        </el-form-item>

        <el-form-item label="密码" prop="pass" class="form-group">
          <div class="input-wrapper">
            <el-input v-model="ruleForm.pass" type="password" autocomplete="off" placeholder="请输入密码" />
          </div>
        </el-form-item>

        <div class="form-options">
          <label class="remember-wrapper">
            <input 
              type="checkbox" 
              v-model="rememberMe"
              class="remember-input"
            >
            <div class="remember-checkbox">
              <i class="fas fa-check check-icon"></i>
            </div>
            <span class="remember-text">记住我</span>
          </label>
          <a href="#" class="forgot-link">忘记密码？</a>
        </div>

        <el-form-item>
            <el-button  @click="submitForm(ruleFormRef)" class="primary-button">
                登录
            </el-button>
            <!-- <el-button @click="resetFormAndNavigateToRegister">注册</el-button> -->
        </el-form-item>

        <div class="bottom-text">
          还没有账号？<a @click="$router.push('/register')" class="link">立即注册</a>
        </div>

      </div>
      

    </el-form>

  </div>
  <!-- <el-container class="background-container">
    <el-header>
      <h3 style="margin-left: 20px;">登录页面</h3>
    </el-header>
    <el-main class="main">
      <img src="/src/assets/logo.jpg" :fit="fit" alt="" class="img">
        <el-form
            ref="ruleFormRef"
            style="max-width: 600px"
            :model="ruleForm"
            status-icon
            :rules="rules"
            label-width="auto"
            class="demo-ruleForm"
        >
            <el-form-item label="账号" prop="account">
                <el-input v-model="ruleForm.account" />
            </el-form-item>

            <el-form-item label="密码" prop="pass">
                <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
            </el-form-item>

            <el-form-item class="button">
                <el-button type="primary" @click="submitForm(ruleFormRef)">
                    提交
                </el-button>
                <el-button @click="resetFormAndNavigateToRegister">注册</el-button>
            </el-form-item>

        </el-form>
    </el-main>
  </el-container> -->
</template>

<style scoped>
.login-container {
  min-height: 70vh;
  display: flex;
  background: #f8fafc;
  border-radius: 30px;
}

/* 左侧展示区样式 */
.showcase {
  flex: 1;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  padding: 40px;
  border-radius: 30px 0 0 30px;
}

.showcase-content {
  max-width: 600px;
  text-align: center;
}

.showcase h1 {
  font-size: 68px;
  font-weight: 600;
  margin-bottom: 20px;
  line-height: 1.2;
}

.showcase p {
  font-size: 20px;
  opacity: 0.9;
  line-height: 1.6;
}

/* 右侧表单区样式 */
.form-container {
  width: 50%;
  max-width: 800px;
  min-width: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-form {
  width: 100%;
  max-width: 440px;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Logo样式 */
.logo {
  text-align: center;
  margin-bottom: 24px;
}

.logo img {
  width: 48px;
  height: 48px;
}

/* 标题样式 */
h2 {
  text-align: center;
  color: #1e293b;
  margin-bottom: 8px;
  font-size: 24px;
  font-weight: 600;
}

.subtitle {
  text-align: center;
  color: #64748b;
  margin-bottom: 32px;
  font-size: 14px;
}

/* 表单组样式 */
.form-group {
  margin-left: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* justify-content: space-between; */
  margin-bottom: 24px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #475569;
  font-size: 14px;
  font-weight: 500;
}

/* 输入框样式 */
input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #1e293b;
  background: #f8fafc;
  transition: all 0.2s ease;
}

input::placeholder {
  color: #94a3b8;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  background: white;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

/* 表单选项样式 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.remember-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.remember-input {
  display: none;
}

.remember-checkbox {
  width: 16px;
  height: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: white;
}

.check-icon {
  font-size: 10px;
  color: white;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.2s ease;
}

.remember-input:checked + .remember-checkbox {
  background: #6366f1;
  border-color: #6366f1;
}

.remember-input:checked + .remember-checkbox .check-icon {
  opacity: 1;
  transform: scale(1);
}

.remember-text {
  font-size: 14px;
  color: #64748b;
}

.forgot-link {
  color: #6366f1;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: #4f46e5;
}

/* 链接样式 */
.link {
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s ease;
}

.link:hover {
  color: #4f46e5;
}

/* 按钮样式 */
.primary-button {
  width: 100%;
  padding: 12px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.primary-button:hover {
  background: #4f46e5;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2);
}

/* 底部文字样式 */
.bottom-text {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: #64748b;
}

/* 响应式设计 */
@media (max-width: 1280px) {
  .showcase h1 {
    font-size: 40px;
  }
  
  .showcase p {
    font-size: 18px;
  }
  
  .form-container {
    padding: 30px;
  }
}

@media (max-width: 1024px) {
  .showcase {
    display: none;
  }
  
  .form-container {
    width: 100%;
    max-width: none;
    min-width: auto;
    padding: 24px;
  }
  
  .login-form {
    max-width: 480px;
    margin: 0 auto;
  }
}

@media (max-width: 640px) {
  .login-container {
    background: white;
  }
  
  .form-container {
    padding: 20px;
  }
  
  .login-form {
    padding: 24px 20px;
    box-shadow: none;
    border-radius: 0;
  }
  
  .logo img {
    width: 40px;
    height: 40px;
  }
  
  h2 {
    font-size: 22px;
  }
  
  .subtitle {
    font-size: 13px;
  }
  
  input {
    padding: 10px 14px;
    font-size: 13px;
  }
  
  .primary-button {
    padding: 10px;
    font-size: 15px;
  }
}

@media (max-height: 700px) {
  .login-form {
    padding: 24px;
  }
  
  .logo {
    margin-bottom: 16px;
  }
  
  .form-group {
    margin-bottom: 16px;
  }
  
  .form-options {
    margin-bottom: 16px;
  }
  
  .bottom-text {
    margin-top: 16px;
  }
}

/* 适配超小屏幕 */
@media (max-width: 360px) {
  .form-container {
    padding: 16px;
  }
  
  .login-form {
    padding: 20px 16px;
  }
  
  input {
    padding: 8px 12px;
  }
  
  .form-options {
    flex-direction: row;
    justify-content: space-between;
    margin-bottom: 16px;
  }
}

/* 适配横屏模式 */
@media (max-height: 500px) and (orientation: landscape) {
  .login-container {
    min-height: auto;
    padding: 20px;
  }
  
  .login-form {
    margin: 20px auto;
  }
}

/* 适配深色模式 */
@media (prefers-color-scheme: dark) {
  .login-container {
    background: #0f172a;
  }
  
  .login-form {
    background: #1e293b;
  }
  
  h2 {
    color: #f8fafc;
  }
  
  .subtitle {
    color: #94a3b8;
  }
  
  label {
    color: #cbd5e1;
  }
  
  input {
    background: #334155;
    border-color: #475569;
    color: #f8fafc;
  }
  
  input::placeholder {
    color: #64748b;
  }
  
  input:focus {
    border-color: #818cf8;
    background: #1e293b;
  }
  
  .remember-checkbox {
    border-color: #475569;
    background: #334155;
  }
  
  .remember-text {
    color: #94a3b8;
  }
  
  .bottom-text {
    color: #94a3b8;
  }
}
</style>
