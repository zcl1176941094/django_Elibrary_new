<template>
    <div class="self_info">
<!--存放个人头像及显示-->
  <el-card>
  <!-- <p> 个人头像显示</p>
    <el-button @click="change_showtype">edit</el-button>--> 


  <div class="item_bock head_p">
     <div class="head_img">
      <img v-bind:src=avatar alt="" height="100px" width="100px">
     </div>
 <!--    <div class="setting_right" @click="uploadHeadImg">
       <div class="caption">更改头像</div>     
     </div>-->
     <!--上传照片-->
    <el-upload
    class="image-uploader"
    action="http://127.0.0.1:8000/userphoto/"
    :multiple="false"

    :show-file-list="false"
    :auto-upload="true"       
    :headers="headers"
    :on-success="handleImageSuccess"
    list-type="picture"

  >
    <el-button type="primary">修改头像</el-button>

    <template #tip>
      <div class="el-upload__tip">
        jpg/png files with a size less than 500kb
      </div>
    </template>
  </el-upload>

</div>




  </el-card>     

<div vbind:class="{'active':isShow}"> 
  <div v-if="isShow" height="100%">
        <el-card class="box-card">
              <div  class="clearfix" >
               <el-button-group
                  style="float: right; padding: 3px 0"
                  type="text">
                  <el-button
                    type="primary"
                    icon="el-icon-edit"
                    size="medium"
                    round
                    @click="change_showtype"
                  >修改信息</el-button>
                </el-button-group>
                <!--个人信息显示-->
              <div>
                <span style="float: left" shadow="hover"><b>个人说明</b></span>
                <br />
                <br />
                <el-divider></el-divider>
                <span>用户ID: </span><span>{{user1.username}}</span>
                <el-divider></el-divider>
                <span>用户名: </span><span>{{user1.nickname}}</span>
                <el-divider></el-divider>
                <span>个人积分: </span><span>{{user1.score}}</span>
                <el-divider></el-divider>
                <span>违规次数: </span>
                      <span v-if="user1.violation>0"><strong style="color:red;"> {{user1.violation}}</strong></span>
                      <span v-else><front style="color:green;">0</front></span>

                <el-divider></el-divider>
                <span>注册时间: </span><span>{{user1.login_time}}</span>
                <el-divider></el-divider>                
              </div>

              </div>


          </el-card>
    </div>
</div>
    

<div v-bind:calss="{'active': isShow}">
  <div v-if="!isShow"  height="100%">
        <el-card class="edit-card">
          <div  class="clearfix">

              <el-button-group
                  style="float: right; padding: 3px 0"
                  type="text">

                <el-button
                    type="primary"
                    icon="el-icon-edit"
                    size="medium"
                    round
                    @click="change_showtype"
                  >返回</el-button>
                  
                  <el-button
                    type="primary"
                    icon="el-icon-check"
                    size="medium"
                    round
                    @click="save_nickname"
                  >确认修改</el-button>
                  
                </el-button-group>
            
            <br/>
            <br/>
            <div>
              <el-row>
                <el-col :span="5"><span>用户名: </span></el-col>
                <el-col :span="12">
                <el-input type="text" v-model="name_input"  @input="inputChange"  placeholder="请输入新用户名"></el-input>
                 </el-col>
              </el-row>
            </div>
          </div>

            </el-card>
  </div>
</div>
    </div>
</template>


<script>

  export default {
    name: 'PersonalCenter',
    data() {
      return {
        name_input:undefined,
        isShow:true,
        //user获取得到的用户信息
        user1:{ username:"",
                nickname:"",
                score: 0,
                violation:0,
                continue:0,
                login_time:"",
        },
        //自定义头像
        avatar: '',
        headers:{Authorization: "Bearer "+this.$store.state.token},
      }
    },
//生命周期，再method、data之后，渲染页面之前
    created(){
            //获取token
        const token=this.$store.state.token;
       // alert(token);
        //发送请求得到个人信息
        this.$axios({ 
            method:"get",
            url: 'http://127.0.0.1:8000/userinfo/',
            headers: {Authorization: "Bearer "+token},
        })
        .then(res=>{
          // this.$message("成功登入获取信息");
           const userinfo1=res.data;
          // alert(userinfo1);
           console.log(userinfo1);
           this.user1={username:userinfo1.username,
                      nickname:userinfo1.nickname,
                      score: userinfo1.score,
                      violation:userinfo1.violation,
                      continue:userinfo1.continue,
                      login_time:userinfo1.login_time,             
           };
        }).catch(err=>{
              this.$message("账号已经过期，请重新登入");
              this.$router.push('/login');
        })
        //获取img地址
        this.init_image();



    },

    methods: {
      //重新获取信息
      re_Get_user(){
        const token=this.$store.state.token;
       // alert(token);
        //发送请求得到个人信息
        this.$axios({ 
            method:"get",
            url: 'http://127.0.0.1:8000/userinfo/',
            headers: {Authorization: "Bearer "+token},
        })
        .then(res=>{
          // this.$message("成功登入获取信息");
           const userinfo1=res.data;
          // alert(userinfo1);
           console.log(userinfo1);
           this.user1={username:userinfo1.username,
                      nickname:userinfo1.nickname,
                      score: userinfo1.score,
                      violation:userinfo1.violation,
                      continue:userinfo1.continue,
                      login_time:userinfo1.login_time,             
           };
          }).catch(err=>{
              this.$message("账号已经过期，请重新登入");
              this.$router.push('/login');
        })

      },

      change_showtype(){
        this.isShow=!this.isShow;
      },

      save_nickname(){
          const token=this.$store.state.token;
       // alert(token);
        //发送请求得到个人信息
        this.$axios({ 
            method:"put",
            url: 'http://127.0.0.1:8000/userinfo/',
            headers: {Authorization: "Bearer "+token},
            data:{ 
              nickname:this.name_input,
            }
        })
        .then(res=>{
          this.$message("成功修改信息");
           const userinfo1=res.data;
          // alert(userinfo1);
           console.log(userinfo1);
           //更新个人资料
           this.user1={username:userinfo1.username,
                      nickname:userinfo1.nickname,
                      score: userinfo1.score,
                      violation:userinfo1.violation,
                      continue:userinfo1.continue,
                      login_time:userinfo1.login_time,             
           };
          })
          .catch(err=>{
              this.$message("账号已经过期，请重新登入");
              this.$router.push('/login');
        })

          this.change_showtype();

      },

   inputChange(e) {
                //强制刷新
                this.$forceUpdate();
            },
//得到img地址
    init_image(){
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
           this.avatar=base_url+res.data.photo;  
        }).catch(err=>{
              this.$message("账号已经过期，请重新登入");
              this.$router.push('/login');
        })

        console.log(this.image_url);

    },
    //上传图片成功
    handleImageSuccess() {
      //this.emitInput(this.tempUrl)
      this.$message("修改头像成功");
      this.init_image();
    },


    },
  }
</script>
<style scoped>
  

  .self_info{ 
      height:"auto";
      width:"100%";
      
  }
  
  .text {
    font-size: 14px;
  }
  .item {
    margin-bottom: 18px;
  }
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: '';
  }
  .clearfix:after {
    clear: both;
  }

  .box-card {
    width: 100%;
    border-radius: 30px;
  }
  .edit-card {
    width: 100%;
    height: 100%;
    border-radius: 30px;
  
  }

  .item_bock {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height:94px;
  width: 300px;
  padding:0px 24px 0px 38px;
  border-bottom: 1px solid #f7f7f7;
  background: #fff;
}
.head_p {
  height:132px;
}
.head_img{
  height: 90px;
}
.head_img img{
  width:90px;
  height:90px;
  border-radius:50px
}
.setting_right{
  display: flex;
  height: 37px;
  justify-content: flex-end;
  align-items: center;
}
.hiddenInput{
  display: none;
}
.caption {
  color: #8F8F8F;
  font-size: 26px;
  height: 37px;
}

</style>