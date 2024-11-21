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
</script>

<template>
  <el-container class="background-container">
    <el-header>
      <h3 style="margin-left: 20px;">注册页面</h3>
    </el-header>
    
    <el-main class="main">
      <img src="/src/assets/logo.jpg" :fit="fit" alt="" class="img">
      <el-form
        ref="ruleFormRef"
        style="max-width: 600px"
        :model="registerForm"
        status-icon
        :rules="rules"
        label-width="auto"
        class="demo-ruleForm"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" autocomplete="off" />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" autocomplete="off" />
        </el-form-item>

        <el-form-item class="button">
          <el-button type="primary" @click="validateForm">
            注册
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-main>
  </el-container>
</template>
  
  <style scoped>
 .el-form-item {
    margin-bottom: 30px; /* 增加输入框之间的间距 */
  }
  .main {
    display: flex;
    flex-direction: column;
    align-items: center; /* 水平居中 */
    justify-content: center; /* 垂直居中 */
    height: 100vh; /* 使容器高度占满整个视口高度 */
  }
  .el-button {
  display: block; /* 使按钮表现为块级元素 */
  margin-left: auto; /* 左边距自动 */
  margin-right: auto; /* 右边距自动 */
}
  .background-container {
    /* background-image: url(C:\\Users\\admin\\Pictures\\Screenshots\\222.png); */
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    min-height: 100vh;
  }
  .input{
    margin-top: 10px;
  }
  .main{
    display: flex;
    flex-direction: column;
    justify-content: left;
    /* align-items: ; */
  }
    .img{
      width: 100px;
      height: 100px;
      margin-left: 20px;
      margin-bottom: 30px;
    }
  </style>