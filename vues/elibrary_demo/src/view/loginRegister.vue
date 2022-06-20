<template>
	<div class="login-register">
		<div class="contain">
			<div class="big-box" :class="{active:isLogin}">
				<div class="big-contain" key="bigContainLogin" v-if="isLogin">
					<div class="btitle">账户登录</div>
					<div class="bform">
						<input type="text" placeholder="账号" v-model="form.username1">
						<input type="password" placeholder="密码" v-model="form.userpwd1">
					</div>
					<!--登入按钮-->
					<button class="bbutton" @click="login">登录</button>
				</div>
				<div class="big-contain" key="bigContainRegister" v-else>
					<div class="btitle">创建账户</div>
					<div class="bform">
						<input type="text" placeholder="用户名" v-model="form.username">
						<input type="password" placeholder="密码" v-model="form.password">
						<input type="password" placeholder="确认密码" v-model="form.repassword">

					</div>
					<!--注册按钮-->
					<button class="bbutton" @click="register">注册</button>
				</div>
			</div>
			<div class="small-box" :class="{active:isLogin}">
				<div class="small-contain" key="smallContainRegister" v-if="isLogin">
					<div class="stitle">你好，朋友!</div>
					<div class="scontent">欢迎来到</div>
					<p class="stitle">电子书分享网站</p>
					<button class="sbutton" @click="changeType">注册</button>
				</div>
				<div class="small-contain" key="smallContainLogin" v-else>
					<div class="stitle">欢迎回来!</div>
					<p class="scontent">与我们保持联系，请登录你的账户</p>
					<button class="sbutton" @click="changeType">登录</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	export default{
		name:'login_register',
		data(){
			return {
				isLogin:true,
				form:{
					username1:'',
					userpwd1:'',
					username:'',
					password:'',
					repassword:''
				}
			}
		},
		//  isLogin:默认界面，点击切换到登陆界面
		methods:{
			changeType() {
				this.isLogin = !this.isLogin
				this.form.username1 = ''
				this.form.userpwd1 = ''
				this.form.username = ''
				this.form.password=''
				this.form.repassword=''
			},

			//登陆模块
			login() {
				const self = this;
				if (self.form.username1 != "" && self.form.userpwd1 != "") {
					self.$axios({
						method:'post',
						url: 'http://127.0.0.1:8000/login/',
						data: {
							username: self.form.username1,
							password: self.form.userpwd1
						}
					})
					//获取信息：有token和其他    
					// token设置 this.$store.commit('$_setToken', userInfo.token);
					//this.$router.push({ name:'homePage' })；  // 跳转到首页
					.then( res => {
						//登入成功的响应码为200
						this.$message("登入成功");
						//若登入成功，有返回token值
						if("token" in res.data){
							//保存token值	
							const loginInfo=res.data;
							this.$store.commit('$_setToken', loginInfo.token);
							if(res.data.is_superuser==false)
								{
									//this.$router.push("/homePage/user");
									this.$router.push("/Search");
								}	
							else{this.$router.push("/admin/Info")}	
						}
					})
					.catch( err => {
						this.$message("登入失败");
						console.log(err);
					})
				} else{
					if(self.form.username1 =='' || self.form.userpwd1=='')
					 {this.$message("填写不能为空！");}
				}
			},
		   //注册模块
			register(){
				//alert("注册前");
				const self = this;
				if(self.form.username != "" && self.form.password == self.form.repassword && self.form.password!= ""){
					//alert("准备开始发送请求");
					self.$axios({
						method:'post',
						url: 'http://127.0.0.1:8000/register/',
						data: {
							username: self.form.username,
							password: self.form.password,
						}
					})
					//进行对json格式的处理
					.then( res => {
						alert("注册成功");
						this.changeType();
					})
					.catch( err => {
						console.log(err); 
						//JSON.parse
						var err_data=err.response.data;
						//账号已注册
						if("username" in err_data){
                              	alert(err_data.username[0]);			
							}
							//账号密码格式问题
						else if( "non_field_errors" in err_data){
								alert(err_data.non_field_errors[0]);
						}
						else{alert("出现未知错误");}	

					})
				} else {
					if(self.form.username == "" || self.form.password == "" || self.form.repassword == "")
					{alert("填写不能为空!");}
					else if(self.form.password != self.form.repassword ){
						alert("俩次输入密码不一致!");
					}
			}
		}
	}
}
</script>


<style scoped="scoped">
	.login-register{
		width: 100vw;
		height: 100vh;
		box-sizing: border-box;
		background-image: url(../assets/images/banner.jpg);
    	background-size: cover;
    	background-position: center;


	}
	.contain{
		width: 60%;
		height: 60%;
		position: relative;
		top: 50%;
		left: 50%;
		transform: translate(-50%,-50%);
		background-color: #fff;
		border-radius: 20px;
		box-shadow: 0 0 3px #f0f0f0,
					0 0 6px #f0f0f0;
	}
	.big-box{
		width: 70%;
		height: 100%;
		position: absolute;
		top: 0;
		left: 30%;
		transform: translateX(0%);
		transition: all 1s;
	}
	.big-contain{
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.btitle{
		font-size: 1.5em;
		font-weight: bold;
		color: rgb(57,167,176);
	}
	.bform{
		width: 100%;
		height: 40%;
		padding: 2em 0;
		display: flex;
		flex-direction: column;
		justify-content: space-around;
		align-items: center;
	}
	.bform .errTips{
		display: block;
		width: 50%;
		text-align: left;
		color: red;
		font-size: 0.7em;
		margin-left: 1em;
	}
	.bform input{
		width: 50%;
		height: 30px;
		border: none;
		outline: none;
		border-radius: 10px;
		padding-left: 2em;
		background-color: #f0f0f0;
	}
	.bbutton{
		width: 20%;
		height: 40px;
		border-radius: 24px;
		border: none;
		outline: none;
		background-color: rgb(57,167,176);
		color: #fff;
		font-size: 0.9em;
		cursor: pointer;
	}
	.small-box{
		width: 30%;
		height: 100%;
		background: linear-gradient(135deg,rgb(57,167,176),rgb(56,183,145));
		position: absolute;
		top: 0;
		left: 0;
		transform: translateX(0%);
		transition: all 1s;
		border-top-left-radius: inherit;
		border-bottom-left-radius: inherit;
	}
	.small-contain{
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.stitle{
		font-size: 1.5em;
		font-weight: bold;
		color: #fff;
	}
	.scontent{
		font-size: 0.8em;
		color: #fff;
		text-align: center;
		padding: 2em 4em;
		line-height: 1.7em;
	}
	.sbutton{
		width: 60%;
		height: 40px;
		border-radius: 24px;
		border: 1px solid #fff;
		outline: none;
		background-color: transparent;
		color: #fff;
		font-size: 0.9em;
		cursor: pointer;
	}
	
	.big-box.active{
		left: 0;
		transition: all 0.5s;
	}
	.small-box.active{
		left: 100%;
		border-top-left-radius: 0;
		border-bottom-left-radius: 0;
		border-top-right-radius: inherit;
		border-bottom-right-radius: inherit;
		transform: translateX(-100%);
		transition: all 1s;
	}
</style>
