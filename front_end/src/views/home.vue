<template>
  <!-- 首页根容器 -->
  <div class="home-container">
    <!-- 欢迎信息 -->
    <h1>欢迎来到首页</h1>
    <!-- Vite logo图片 -->
    <img src="/vite.svg" alt="Vite logo">
    <!-- 退出登录按钮 -->
    <button @click="handleLogout">退出登录</button>
  </div>
</template>

<script setup>
// 导入路由组件
import { useRouter } from 'vue-router'

// 创建路由实例
const router = useRouter()

// 处理退出登录的方法
const handleLogout = () => {
  // 跳转回登录页
  router.push('/login')
}
</script>

<style scoped>
/* 首页容器样式 */
.home-container {
  padding: 20px;
  text-align: center;
}

/* 图片样式 */
img {
  width: 100px;
  margin: 20px 0;
}

/* 按钮样式 */
button {
  padding: 10px 20px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 按钮悬停效果 */
button:hover {
  background: #d32f2f;
}
</style>