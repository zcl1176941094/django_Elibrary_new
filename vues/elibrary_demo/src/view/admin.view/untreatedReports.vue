<template>
    

    <div style="position: relative; height:0%">
       <!-- <p>上传历史</p>-->
            <br><br>
        <div>
            <el-table :data="page.dataList | forListTime" 
                    style="width:auto;
                    margin-left:auto;margin-right:auto;"
                    stripe >

                <el-table-column label="序号" type="index" :index="getIndex" width="50px" align="center"></el-table-column>
                <el-table-column prop="fid" width="100px" label="书籍编号" align="center"></el-table-column>
                <el-table-column prop="range" width="100px" label="范围" align="center" margin-left="20px" ></el-table-column>
                <el-table-column prop="details" width="400px"  label="原因"  align="center"></el-table-column>

                <el-table-column prop="Reporttime" label="举报时间" width="200px" align="center"></el-table-column>

                <el-table-column align="right" margin-left="10px">
                <!-- <template #header>
                    <el-input v-model="search" size="small" placeholder="Type to search" />
                     </template>--> 
                    <template #default="scope" >
         <!--               <el-button size="small" @click="handlPreview(scope.$index, scope.row)"  type="Info" plain>具体举报信息</el-button> -->
                        <el-button size="small" @click="handlPreview(scope.$index, scope.row)"  type="Info" plain>查看书籍</el-button>
                        <el-button size="small" @click="handlEdit(scope.$index, scope.row,0)"  type="success" >正常</el-button>
                        <el-button size="small" @click="handlEdit(scope.$index, scope.row,1)"  type="danger" >违规</el-button>
   <!--     暂时未实现   <el-button
                            size="small"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">删除</el-button>     -->
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
                    url: "http://127.0.0.1:8000/search_undo_msg/?page="+this.page.pageNo+"&page_size="+this.page.pageSize,
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


            //封禁书籍

            banBook(bfid){
                if(bfid){
                this.$axios({
                    method:"get",
                    url:"http://127.0.0.1:8000/ban_book/"+bfid+"/",
                    headers: {Authorization: "Bearer "+this.$store.state.token},
                })
                .then(res=>{
                    //console.log(res)
                    //alert("操作成功")
                    this.$message("封禁成功")
                })
                .catch(err=>{
                    console.log(err)
                })




                }
            },

            //书籍操作 adsult(0:)(1:)
            handlEdit(index,row,adresult){
                //this.$message("处理中")
                this.$axios({
                    method:"post",
                    url:"http://127.0.0.1:8000/manage_report/"+row.reportid+"/",
                    data:{result:adresult},
                    headers: {Authorization: "Bearer "+this.$store.state.token},
                })
                .then(res=>{
                    //console.log(res)
                    //alert("操作成功")
                    if(adresult==0)
                    {this.$message("处理成功")}
                    else{
                        this.banBook(row.fid);
                    }

                    
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
		            item.Reporttime= moment(item.Reporttime).format('YYYY-MM-DD hh:mm:ss');    
		                return item;})
		    }
		},


    }



</script>


<style>



</style>