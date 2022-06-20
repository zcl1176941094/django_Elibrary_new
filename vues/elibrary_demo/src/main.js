// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'

//引入element-UI并使用
import ElementUi from 'element-ui';
//import { Collection } from '@element-plus/icons-vue/dist/types'
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUi);


import './assets/css/icon.css'

Vue.config.productionTip = false

//每次向后端请求携带 头信息
//axios.interceptors.request.use(
  
  //config => {
   // if (localStorage.getItem('token')) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
 //     config.headers.Authorization = `token ${localStorage.getItem('token')}`;
  //  }
 //   return config;
 // },
 // err => {
 //   return Promise.reject(err);
 // });

 import store from "./store";
 //store  保存登陆状态

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,    //将 store 注册到 Vue 根实例
  components: { App },
  template: '<App/>'
})
