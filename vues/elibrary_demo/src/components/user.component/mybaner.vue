<template>
    <div class="header">
        <div class="logo">电子书共享网站</div>
        <div class="header-right">
            <div class="header-user-con">
                <!-- 消息中心 -->
                <div class="btn-bell">
                    <el-tooltip effect="dark" :content="message?`有${message}条未读消息`:`消息中心`" placement="bottom">
                        <router-link to="/homePage/messages">
                            <i class="el-icon-bell"></i>
                        </router-link>
                    </el-tooltip>
                    <span class="btn-bell-badge" v-if="message"></span>
                </div>
                <!-- 用户头像 -->
                <div class="user-avator">
                    <!--"../../assets/images/sample_pic.png" -->
                    <el-image :src="image_url" />
                </div>
                <!-- 用户名下拉菜单 -->
                <el-dropdown class="user-name" trigger="click" @command="handleCommand">
                    <span class="el-dropdown-link">
                        {{username}}
                        <i class="el-icon-caret-bottom"></i>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item  command="user">个人中心</el-dropdown-item>
                            <el-dropdown-item divided command="upfile">上传文件</el-dropdown-item>
                            <el-dropdown-item divided command="loginout">退出登录</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>
    </div>
</template>




<script>
import { MessageBox } from "mint-ui";
import '../../assets/css/icon.css'
//import { computed, onMounted } from "vue";
//import { useStore } from "vuex";
//import { useRouter } from "vue-router";
export default {
    name:'mybaner1',
    data() {
        const message=0;
        const username="567";
        // 用户名下拉菜单选择事件


        return {
            username,
            message,
         //   collapse,
         //   collapseChage,
         //   handleCommand,
         image_url:"",
        };
 



        },
    created(){
            //获取token
        const token=this.$store.state.token;
        const base_url="http://127.0.0.1:8000";
       // alert(token);
        //发送请求得到个人信息
        this.$axios({ 
            method:"get",
            url: 'http://127.0.0.1:8000/userinfo/',
            headers: {Authorization: "Bearer "+token},
        })
        .then(res=>{
          // this.$message("成功登入获取信息");
           this.username=res.data.nickname;   
        }).catch(err=>{
              this.$message("账号已经过期，请重新登入");
              this.$router.push('/login');
        })
        //获取图片信息
        this.$axios({ 
            method:"get",
            url: 'http://127.0.0.1:8000/userphoto/',
            headers: {Authorization: "Bearer "+token},
        })
        .then(res=>{
          // this.$message("成功登入获取信息");
           this.image_url=base_url+res.data.photo;  
        }).catch(err=>{
              this.$message("账号已经过期，请重新登入");
              this.$router.push('/login');
        })

        console.log(this.image_url);

    },
     
    methods:{ 
        handleCommand (command)  {
            const self=this;
            if (command == "loginout") {
                //localStorage.removeItem("token");
                //删除token
                this.$store.commit('$_removeStorage');    // 清除登录信息
                this.$router.push('/login');
            } else if (command == "user") {
                //this.$router.push("/homePage/user");
                let {href} = this.$router.resolve({
                path: "/homePage/user",//新页面地址
                //query: { id: localStorage.id }//携带的参数
                });

                window.open(href, '_blank');

            }
            else if (command == "upfile") {
                let {href} = this.$router.resolve({
                path: "/upfile/",//新页面地址
                //query: { id: localStorage.id }//携带的参数
                });

                window.open(href, '_blank');
            }
        },  
    }
}
</script>



<style scoped="scoped">


.header {
    position: relative;
    width: 100%;
    height: 70px;
    font-size: 22px;
    margin: 0px;
    padding: 0px;
    color: #fff;
    background-color: #272727;
}
.logo {
    float: left;
    width: 250px;
    line-height: 70px;
}
.header-right {
    float: right;
    padding-right: 50px;
}
.header-user-con {
    display: flex;
    height: 70px;
    align-items: center;
}
.btn-fullscreen {
    transform: rotate(45deg);
    margin-right: 5px;
    font-size: 24px;
}
.btn-bell,
.btn-fullscreen {
    position: relative;
    width: 30px;
    height: 30px;
    text-align: center;
    border-radius: 15px;
    cursor: pointer;
}
.btn-bell-badge {
    position: absolute;
    right: 0;
    top: -2px;
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background: #f56c6c;
    color: #fff;
}
.btn-bell .el-icon-bell {
    color: #fff;
}
.user-name {
    margin-left: 10px;
}
.user-avator {
    margin-left: 20px;
}
.user-avator .el-image {
    display: block;
    width: 40px;
    height: 40px;
    border-radius: 50%;
}
.el-dropdown-link {
    color: #fff;
    cursor: pointer;
}
.el-dropdown-menu__item {
    text-align: center;
}
</style>
