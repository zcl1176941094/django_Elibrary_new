<template>
  <div class="common-layout" >
    <el-container    direction="vertical">
      <el-header>
        <adbaner></adbaner>
      </el-header>
      <el-container>
        <el-aside >
          <!-- 自定义主键的使用不支持_符号-->
          <adaside></adaside>
        </el-aside>
        <el-container  direction="vertical">
          <el-main>
            <adcontent></adcontent>
          </el-main>
          <el-footer >
            <adfooter></adfooter>
          </el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>



<script>
import adbaner from "./admin.view/component/adbaner.vue"
import adaside from "./admin.view/component/adaside.vue"
import adcontent from "./admin.view/component/adcontent.vue"
import adfooter from "./admin.view/component/adfooter.vue"

export default {
    name: "administrater",
    components: { adbaner,adaside,adcontent,adfooter },
    
    data(){
        return {}
    },
    
    method:{

    },

    setup() {
        
    },




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
  background-color: 			Beige;
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
  background-color: #0f3e6d;
}  


</style>


