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
  <el-container class="background-container">
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
