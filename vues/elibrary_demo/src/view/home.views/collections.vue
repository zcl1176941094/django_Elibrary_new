<template>
    
    <div style="position: relative; height:80%">
       <!-- <p>收藏列表</p>-->
            <br><br>
        <div>
            <el-table :data="page.dataList | forListTime" 
                    style="width:80%;
                    margin-left:auto;margin-right:auto;"
                    stripe >

                <el-table-column label="序号" type="index" :index="getIndex" width="100px" align="center"></el-table-column>
                <el-table-column prop="fname" label="书籍名" width="400px"  align="center"></el-table-column>


                <el-table-column prop="download_time" label="下载日期" width="150px"  align="center"></el-table-column>
                <el-table-column prop="ave_score" label="评分" width="50px"></el-table-column>

                <el-table-column align="right">
                <!-- <template #header>
                    <el-input v-model="search" size="small" placeholder="Type to search" />
                     </template>--> 
                    <template #default="scope" margin-right="20px">
                
                        <el-button size="small" @click="handlPreview(scope.$index, scope.row)" v-if="scope.row.isvalid==true" type="success" plain>查看</el-button>
                        <el-button size="small" @click="handlPreview(scope.$index, scope.row)" v-if="scope.row.isvalid==false" type="warning" plain>查看</el-button>
                       <el-button
                            size="small"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">取消收藏</el-button>
                    </template>     
                </el-table-column>

            </el-table>
        </div>

        <div>
            <el-pagination 
                small background
                layout="total,prev, pager, next ,jumper" 
                @current-change="ResetPageNo"
                :current-page="page.pageNo"
                :page-size="page.pageSize"
                :total="page.RowsTotal" >
            </el-pagination> 
        </div>   


    </div>

</template>





<script>
//自定义过滤器（将时间戳转换成年月日时分秒）需要用到的
import moment from 'moment'

    export default{
        name:"collectionList",
        data(){
            return {
                page:{
                    pageTotal:0, //总页数
                    pageSize:7,  //每页数据量
                    RowsTotal:0  ,  //总数据量                
                    dataList:[], //该页数据
                    pageNo:1,    //页数
                },

                tableHeight: "",//表格高度
            }
        },


        methods:{

            getIndex(i){return (this.page.pageNo-1)*this.page.pageSize+i+1;},

            //获取当前页的数据
            getPageList(i){
                this.page.pageNo= i || this.page.pageNo  ; 
                //上传文件历史
                this.$axios({
                    method:"get",
                    url: "http://127.0.0.1:8000/collections/?page="+this.page.pageNo+"&page_size="+this.page.pageSize,
                    headers: {Authorization: "Bearer "+this.$store.state.token},
                })
                .then(res=>{
                   // alert("获取成功")
                    console.log(res.data)
                    this.page.dataList=res.data.data;      // 该页数据
                    this.page.pageTotal=res.data.pageSum;    // 总页数
                    this.page.RowsTotal=res.data.sum;        //总数据量
                    this.page.pageSize=res.data.pagesize;    //每页数据
                })
                .catch(err=>{
                    console.log(err);
                })

            },


            //修改页数
            ResetPageNo(index){
                this.getPageList(index);
            },

            //查看文件
            handlPreview(index,row){
                //console.log(index,row)
                let {href} = this.$router.resolve({
                path: "/book/"+row.fid,//新页面地址
                //query: { id: localStorage.id }//携带的参数
                });

                window.open(href, '_blank');
            },
            //取消收藏
            handleDelete(index,row){
              this.$axios({
                    method:"get",
                    url: "http://127.0.0.1:8000/cancel_collection/"+row.fid+"/",
                    headers: {Authorization: "Bearer "+this.$store.state.token},
                })
                .then(res=>{
                    this.$message("删除成功")
                    //更新List列表
                    this.getPageList();
                })

                .catch(err=>{
                    console.log(err)
                })
 

            }


        },

        created(){
            //初始化获得第一页的文件
            this.getPageList();

        },


        filters: {
		    forListTime(listData){
		        return listData.filter(function (item) {
		            item.download_time= moment(item.download_time).format('YYYY-MM-DD hh:mm:ss');    
		                return item;})
		    }
		},




    }



</script>


<style>



</style>