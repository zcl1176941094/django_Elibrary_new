import Vue from 'vue'
import Router from 'vue-router'
//原生页面
import HelloWorld from '@/components/HelloWorld'
import loginRegister from '@/view/loginRegister.vue'
import homePage from '@/view/homePage.vue'
//路由渲染的页面
import myfiles from "@/view/home.views/myfiles.vue"
import collections from "@/view/home.views/collections.vue"
import userInformation from "@/view/home.views/userInformation.vue"
import downLoadHistory from "@/view/home.views/downLoadHistory.vue"
import messages from "@/view/home.views/mymessage.vue"
import bookInfo from "@/view/bookInfo.vue"

//引入使用axios
//import axios from 'axios'; 
//import VueAxios from 'vue-axios'; 
//Vue.use(VueAxios,axios);

// 引入依赖并全局注册
import axios from 'axios'
Vue.prototype.$axios = axios


//引入使用Router
Vue.use(Router)



import upload_file from "../components/user.component/upfile.vue"
import test from "../components/book.component/test.vue"

import adminis from "../view/administrator.vue" 
import treatedReports from "../view/admin.view/treatedReports"
import untreatedReports from "../view/admin.view/untreatedReports"
import adminInfo from "../view/admin.view/adInformation"

import search from "../view/mysearch.vue"


//测试无用


//配置路由环境
export default new Router({
  routes: [

    {
      path:"/search",
      name:"搜索界面",
      component:search,
    },


    {
      path:"/test",
      name:"打分测试",
      component:test
    },
    {
      path:'/upfile',
      name:"上传文件",
      component:upload_file,
    },
    { 
      path: '/login',
      name: '登入注册',
      component: loginRegister,
      meta: {
        title: '登入',
        levelList: []
      },
    },
    //     个人信息页面
    {
      path:'/homePage',
      name:'主页面',
      component: homePage,
      children:[
        {
          path:'/homePage/user',
          name:"个人信息",
          component:userInformation,
          meta: {
            title: '个人中心',
            levelList: []
          },
        },
        {
          path:'/homePage/collections',
          name:'收藏列表',
          component:collections,
          meta: {
            title: '个人收藏',
            levelList: []
          }
        },
        {
          path:'/homePage/myfiles',
          name:"我的文件",
          component:myfiles,
          meta: {
            title: '我的文件',
            levelList: []
          }
        },
        {
          path:'/homePage/downLoadHistory',
          name:"下载历史",
          component:downLoadHistory,
          meta: {
            title: '下载历史',
            levelList: []
          },
        },
        {
          path:'/homePage/messages',
          name:"消息中心",
          component:messages,
          meta: {
            title: '消息中心',
            levelList: []
          },
        }

      ]
    },

    //管理员页面

    {
        path:"/admin",
        name:"管理员页面",
        component:adminis,
        children:[
          {
            path:"/admin/Info",
            name:"个人信息",
            component:adminInfo,
        },
          {
              path:"/admin/untreated",
              name:"未处理举报信息",
              component:untreatedReports,
          },
          {
              path:"/admin/treated",
              name:"处理过的举报信息",
              component:treatedReports,
          }
        ]
    },

    //      书籍信息
    {
      path:'/book/:fid',
      name:"书籍信息",
      component:bookInfo
    },
    {
      path: '/123',
      name: 'HelloWorld',
      component: HelloWorld
    },

    { //路由重定向
      path: '*',
      name: 'any', // 名字在“命名路由”中使用，但是不介绍
      redirect: '/login'
    },

  ]
})
