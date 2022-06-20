<template>
  <div>
           
      <el-menu :default-active="$route.path"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          router
          height="100%">
<el-image :src="img_url" style="height:150px" />

          <el-menu-item index="/admin/Info">
        
              <span >个人信息</span>
          
          </el-menu-item>
        <el-menu-item index="/admin/untreated">
              <span >未处理</span>
          </el-menu-item>  
          <el-menu-item index="/admin/treated">
              <span >已处理</span>
          </el-menu-item>

        </el-menu>
    </div>

</template>


<script>



//导航栏的使用
	export default{
		name:'adaside',
      data(){
          return {
              img_url:"http://127.0.0.1:8000/media/img1/mylogo.png"
            }
        },
        methods:{

        }
    }
</script>


<style  scoped>

.aside_set{ 
    background-color:"#545c64";
    height:"100%";
    padding: 0px;
    margin: 0px;
    
}




</style>