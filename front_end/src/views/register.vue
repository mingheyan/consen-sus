<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

const router = useRouter();
const ruleFormRef = ref<FormInstance | null>(null);

// 表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
});

// 验证规则
const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 15, message: '用户名长度在 3 到 15 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度不能少于 8 位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: (rule, value, callback) => {
      if (value !== registerForm.password) {
        callback(new Error('两次输入密码不一致'));
      } else {
        callback();
      }
    }, trigger: 'blur' }
  ],
});

// 表单验证
const validateForm = async () => {
  if (!ruleFormRef.value) return;
  try {
    const valid = await ruleFormRef.value.validate();
    if (valid) {
      const response = await axios.post('你的注册API地址', {
        username: registerForm.username,
        password: registerForm.password,
      });
      if (response.status === 200) {
        console.log('注册成功:', response.data);
        // 注册成功后的逻辑，例如路由跳转
        router.push('/login');
      } else {
        console.error('注册失败:', response.data);
      }
    } else {
      console.log('表单验证失败');
    }
  } catch (error) {
    console.error('注册时发生错误:', error);
  }
};

// 重置表单
  const resetForm = () => {
    if (ruleFormRef.value) {
      ruleFormRef.value.resetFields();
    }
  };
  const goToLogin = () => {
    router.push('/')
  };
</script>

<template>
  <div class="register-container">

    <!-- 左侧展示区 -->
    <div class="showcase">
      <div class="showcase-content">
        <h1>开始您的旅程</h1>
        <p>加入我们，探索更多可能</p>
      </div>
    </div>
    <!-- 右侧注册表单 -->
    <el-form
        ref="ruleFormRef"
        style="max-width: 600px"
        :model="registerForm"
        status-icon
        :rules="rules"
        label-width="auto"
        class="form-container"
      >
      <div class="register-form">
        <div class="logo">
          <img src="/src/assets/logo.jpg"  alt="logo" >
        </div>
        <h2>创建账号</h2>
        <p class="subtitle">请填写以下信息完成注册</p>

        <el-form-item label = "用户名" prop="username" class="form-group">
          <!-- <label class="form-label">用户名</label> -->
          <div class="input-wrapper">
            <el-input v-model="registerForm.username" placeholder="请输入用户名" />
          </div>
        </el-form-item>

        <el-form-item label = "密码" prop="password" class="form-group">
          <!-- <label class="form-label">密码</label> -->
          <div class="input-wrapper">
            <el-input v-model="registerForm.password" type="password" autocomplete="off" placeholder="请输入密码" />
          </div>
        </el-form-item>

        <el-form-item label = "确认密码" prop="confirmPassword" class="form-group">
          <!-- <label class="form-label">确认密码</label> -->
          <div class="input-wrapper">
            <el-input v-model="registerForm.confirmPassword" type="password" autocomplete="off" placeholder="请再次输入密码" />
          </div>
        </el-form-item>

        <div class="terms">
          <label class="checkbox-wrapper">
            <input type="checkbox" class="checkbox-input">
            <span class="checkbox-custom"></span>
            <span class="terms-text">
              我已阅读并同意
              <a href="#" class="link">用户协议</a>
              和
              <a href="#" class="link">隐私政策</a>
            </span>
          </label>
        </div>

        <div class="bottom-text">
          已有账号？<a @click="goToLogin" class="link">立即登录</a>
        </div>

        <el-form-item class="button">
          <el-button class="primary-button" @click="validateForm">
            注册
          </el-button>
        </el-form-item>
      </div>
    </el-form>

  </div>


</template>
  
<style scoped>
.register-container {
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

.register-form {
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

/* 表单组样式优化 */
.form-group {
  margin-left: 20px;
  display: flex;
  /* justify-content: center; */
  align-items: center;
  /* justify-content: space-between; */
  margin-bottom: 24px;
}

.form-label {
  display: block;
  color: #1e293b;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
}

/* 输入框样式优化 */
input {
  width: 100%;
  height: 44px;
  padding: 0 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  background: #fff;
  transition: all 0.2s ease;
}

input::placeholder {
  color: #94a3b8;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* 复选框样式 */
.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border: 2px solid #e2e8f0;
  border-radius: 4px;
  position: relative;
  transition: all 0.2s ease;
}

.checkbox-input:checked + .checkbox-custom {
  background: #6366f1;
  border-color: #6366f1;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.terms {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 12px;
}

.terms-text {
  font-size: 14px;
  color: #64748b;
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
  margin-top: 12px;
  margin-bottom: 8px;
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
  
  .register-form {
    max-width: 480px;
    margin: 0 auto;
  }
}

@media (max-width: 640px) {
  .register-container {
    background: white;
  }
  
  .form-container {
    padding: 20px;
  }
  
  .register-form {
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
  
  .terms {
    font-size: 13px;
  }
}

@media (max-height: 700px) {
  .register-form {
    padding: 24px;
  }
  
  .logo {
    margin-bottom: 16px;
  }
  
  .form-group {
    margin-bottom: 16px;
  }
  
  .terms {
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
  
  .register-form {
    padding: 20px 16px;
  }
  
  input {
    padding: 8px 12px;
  }
  
  .terms {
    font-size: 12px;
  }
  
  .checkbox-wrapper {
    align-items: flex-start;
  }
  
  .checkbox-custom {
    margin-top: 3px;
  }
}

/* 适配横屏模式 */
@media (max-height: 500px) and (orientation: landscape) {
  .register-container {
    min-height: auto;
    padding: 20px;
  }
  
  .register-form {
    margin: 20px auto;
  }
  
  .form-group {
    margin-bottom: 12px;
  }
}

/* 适配深色模式 */
@media (prefers-color-scheme: dark) {
  .register-container {
    background: #0f172a;
  }
  
  .register-form {
    background: #1e293b;
  }
  
  h2 {
    color: #f8fafc;
  }
  
  .subtitle {
    color: #94a3b8;
  }
  
  .input-label {
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
  
  .checkbox-custom {
    border-color: #475569;
  }
  
  .terms-text {
    color: #94a3b8;
  }
  
  .bottom-text {
    color: #94a3b8;
  }
}

/* 打印样式优化 */
@media print {
  .register-container {
    background: white;
  }
  
  .showcase {
    display: none;
  }
  
  .register-form {
    box-shadow: none;
    max-width: 100%;
    padding: 0;
  }
  
  .primary-button {
    display: none;
  }
  
  input {
    border: 1px solid #000;
  }
}
</style>