<template>
  <div class="common-layout" >
    <el-container    direction="vertical">
      <el-header>
        <mybaner1></mybaner1>
      </el-header>
      <el-container>
        <el-aside >
          <!-- 自定义主键的使用不支持_符号-->
          <mymainalside1></mymainalside1>
        </el-aside>
        <el-container  direction="vertical">
          <el-main>
            <mycontent1></mycontent1>
          </el-main>
          <el-footer >
            <myfooter1></myfooter1>
          </el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>


<script>
//导入组件
import mybaner1 from "../components/user.component/mybaner.vue"
import myfooter1 from "../components/user.component/myfooter.vue"
import mycontent1 from "../components/user.component/mycontent.vue"
import mymainalside1 from "../components/user.component/mymain_alside.vue"

	export default{
		name:'home',
        data(){
          return {}
        },
        methods:{
          
        },
        //组件的引入
        components:{
            mybaner1,myfooter1,mycontent1,mymainalside1
        }
    }
</script>


<style  scoped="scoped">

.common-layout{ 
  position: absolute;
  margin: 0px;
  padding: 0px;
  width: 100%;
  height : 100%;
}

.el-container{
    height: 100%;
    padding: 0px;
    margin: 0px;
}


.el-header{
  display:flex;
  /**两端对齐**/
  width:100%;
  /**垂直方向居中对齐**/
  align-items:center;
  padding: 0px;
  margin: 0px;
  background-color: "#019858";

}

.el-main{ 
  width:'auto';
  padding: 0px;
  margin: 0px;
  height:100%;
  background-color: #feeeed;
}

.el-aside {
  padding: 0px;
  margin: 0px;
  height :100%;
  width:"200px";
  background-color: #545c64;
}

.el-footer{
  height:"20px";
  width:'auto';
  padding: 0px;
  margin: 0px;
  background-color: #293047;
}  


</style>

