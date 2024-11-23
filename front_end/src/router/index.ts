import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import login from '../views/login.vue';
import register from '../views/register.vue';
import home from '../views/home.vue';
 
const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'login',
    component: login,
    // children: [
    //   // 添加子路由
    //   // {
    //   //   path: '/example',
    //   //   name: 'Example',
    //   //   component: ExampleComponent,
    //   // },
    // ],
  },
  {
    path: '/register',
    name: 'register',
    component: register,
    // children: [
    //   // 添加子路由
    //   // {
    //   //   path: '/example',
    //   //   name: 'Example',
    //   //   component: ExampleComponent,
    //   // },
    // ],
  },
  {
    path: '/home',
    name: 'home',
    component: home,
    // children: [
    //   // 添加子路由
    //   // {
    //   //   path: '/example',
    //   //   name: 'Example',
    //   //   component: ExampleComponent,
    //   // },
    // ],
  },
];
 
const router = createRouter({
  history: createWebHistory(),
  routes,
});
 
export default router;