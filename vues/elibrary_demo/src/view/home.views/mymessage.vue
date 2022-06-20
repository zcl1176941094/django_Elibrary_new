<template>
    
    <div style="position: relative; height:80%">
       <!-- <p>下载历史</p>-->
       <br/><br/>
       <div style="float:right;margin-right:50px;">
            <el-switch
                v-model="switch_report"
                active-text="被举报信息"
                inactive-text="举报信息"
                @change="changeSwitch()">
            </el-switch>
        </div>
            <br><br>

            <!--调整高度，背景色-->
        <div v-if="switch_report">
            <!--   被举报信息表-->
            <el-table :data="page.dataList | forListReportTime" 
                    style="width:80%;
                    margin-left:auto;margin-right:auto;"
                    stripe >

                <el-table-column label="序号" type="index" :index="getIndex" width="50px" align="center"></el-table-column>
                <el-table-column prop="fid" label="书籍编号" width="50px"  align="center"></el-table-column>
                <el-table-column prop="range" width="100px" label="范围" align="center" margin-left="20px" ></el-table-column>
                <el-table-column prop="details" width="500px"  label="原因"  align="center"></el-table-column>

                <el-table-column prop="Reporttime" label="举报时间" width="150px"  align="center"></el-table-column>


                <el-table-column align="right">
                    <template #header>
                    <!--<el-input v-model="search" size="small" placeholder="Type to search" />-->
                        <p style="margin-right:30px;">处理进度</p>
                    </template>
                    <template #default="scope">
                        <div v-if="scope.row.isdealt==true" style="margin-right:30px" >
                            <hy-button  v-if="scope.row.result=='未违规'" type="text" size="small"> <strong style="color:green;">正常</strong> </hy-button>            
                            <hy-button  v-if="scope.row.result=='违规'" type="text" size="small"> <strong style="color:red;">违规</strong> </hy-button>                        
                        </div>
                    
   <!--     暂时未实现   <el-button
                            size="small"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">删除</el-button>     -->
                    </template>     
                </el-table-column>

            </el-table>
        </div>




        <div v-else>
            <!--举报信息-->
            <el-table :data="page.dataList | forListReportTime" 
                    style="width:80%;
                    margin-left:auto;margin-right:auto;"
                    stripe >

                <el-table-column label="序号" type="index" :index="getIndex" width="50px" align="center"></el-table-column>
                <el-table-column prop="fid" label="书籍编号" width="50px"  align="center"></el-table-column>
                <el-table-column prop="range" width="50px" label="范围" align="center" margin-left="20px" ></el-table-column>
                <el-table-column prop="details" width="450px"  label="原因"  align="center"></el-table-column>

                <el-table-column prop="Reporttime" label="举报时间" width="150px"  align="center"></el-table-column>


                <el-table-column align="right">
                    <template #header>
                    <!--<el-input v-model="search" size="small" placeholder="Type to search" />-->
                        <p style="margin-right:30px;">处理进度</p>
                    </template>
                    <template #default="scope">
                        <div v-if="scope.row.isdealt==true" style="margin-right:30px" >
                            <hy-button  v-if="scope.row.result=='未违规'" type="text" size="small"> <strong style="color:green;">正常</strong> </hy-button>            
                            <hy-button  v-if="scope.row.result=='违规'" type="text" size="small"> <strong style="color:red;">违规</strong> </hy-button>                        
                        </div>                        
                        <div v-if="scope.row.isdealt==false" style="margin-right:30px"><strong style="color:gray;">审核中</strong></div>
                      
                    </template>     
                </el-table-column>

            </el-table>


        </div>



        <!-----------------------分页框--------------------------->
        <div style="margin-bottom;20px;">
            <!--位置布局在哪里？-->
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
                //添加俩条基础url{获取举报信息和被举报信息}
                switch_report:true,
                page:{
                    pageTotal:0, //总页数
                    pageSize:8,  //每页数据量
                    RowsTotal:0  ,  //总数据量                
                    dataList:[], //该页数据
                    pageNo:1,    //页数
                },
                //举报与被举报的表的url
                report_url:{
                    report:"http://127.0.0.1:8000/get_report/?page=",
                    reported:"http://127.0.0.1:8000/get_reported/?page=",
                },

                tableHeight: "",//表格高度
            }
        },


        methods:{

            getIndex(i){return (this.page.pageNo-1)*this.page.pageSize+i+1;},

            //获取当前页的数据
            getPageList(i){
                this.page.pageNo= i || this.page.pageNo  ;
                let  baseurl= this.switch_report==true? this.report_url.reported : this.report_url.report;
                //上传文件历史
                this.$axios({
                    method:"get",
                    url: baseurl+this.page.pageNo+"&page_size="+this.page.pageSize,
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

            //切换时候的相对应修改
            changeSwitch(){
                //alert("11111")
                this.getPageList(1);
            }

        },

        created(){
            //初始化获得第一页的文件
            this.getPageList();

        },


        filters: {
		    forListReportTime(listData){
		        return listData.filter(function (item) {
		            item.Reporttime= moment(item.Reporttime).format('YYYY-MM-DD hh:mm:ss');    
		                return item;})
		    },

		},




    }



</script>


<style>



</style>