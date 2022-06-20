<template>
<div>
        <!--内容页面自动根据路由渲染-->
      <router-view></router-view>  
</div>
    
</template>


<script>
//在导航栏选择后的渲染界面
	export default{
		name:'mycontent1',
        data(){
            return {}
        },
        methods:{

        }
    }
</script>


<style scoped="scoped">
</style>