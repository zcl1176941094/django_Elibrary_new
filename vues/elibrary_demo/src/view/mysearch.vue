<template>
<div style="background-color:#f6f5ec;height:100px;">
  <!----------------->
  <mybaner/>
  <br/><br/><br/>
    <div>
        <el-form :inline="true"> 
        <el-form-item label-width="1000px">
            <el-input v-model="input.name" size=medium placeholder="请输入查询书名" style="width:400px;"></el-input>
        </el-form-item>

        <el-form-item label-width="200px" >
            <el-select v-model="input.category" placeholder="种类" size=small style="width:150px;">
            <el-option label="数学" value='数学'></el-option>
            <el-option label="外语" value='外语'></el-option>
            <el-option label="物理" value='物理'></el-option>
            <el-option label="化学" value='化学'></el-option>
            <el-option label="文学" value='文学'></el-option>
            <el-option label="生物" value='生物'></el-option>
            <el-option label="计算机" value='计算机'></el-option>
             <el-option label="其他" value=''></el-option>           
            </el-select>
        </el-form-item>

        <el-form-item>
        <el-button type="primary" @click="onSubmit()">查询</el-button>
        </el-form-item>

        
        </el-form>
    </div>
<!--搜寻结果显示-->
     <div v-if="chat">
            <el-table :data="page.dataList" 
                    style="width:80%;
                    margin-left:auto;margin-right:auto;"
                    stripe >

                <el-table-column label="序号" type="index" :index="getIndex" width="100px" align="center"></el-table-column>
                <el-table-column prop="fname" label="书籍名" width="400px"  align="center"></el-table-column>
                <el-table-column prop="download_times" label="下载次数" width="100px"  align="center"></el-table-column>
                <el-table-column prop="ave_score" label="评分" width="50px"></el-table-column>

                <el-table-column align="right">
                    <template #default="scope" margin-right="20px">
                
                        <el-button size="small" @click="handlPreview(scope.$index, scope.row)" v-if="scope.row.isvalid==true" type="success" plain>查看</el-button>
                        <el-button size="small" @click="handlPreview(scope.$index, scope.row)" v-if="scope.row.isvalid==false" type="warning" plain>查看</el-button>
   <!--     暂时未实现   <el-button
                            size="small"
                            type="danger"
                            @click="handleDelete(scope.$index, scope.row)">删除</el-button>     -->
                    </template> 
                </el-table-column>

            </el-table>
        </div>


          <!-------组件：日常推荐书籍--------->
      <div style="align:center;" v-else>

        <dailyBooks></dailyBooks>

  
    </div>


</div>
</template>


<script>
import dailyBooks from "./search.component/daily_books.vue"
import mybaner from "../components/user.component/mybaner.vue"


  export default {
    components:{dailyBooks,mybaner},
    data() {
      return {
          chat :false,
          
          input:{
              name:'',
              category:''
          }, 
           page:{
                    pageTotal:0, //总页数
                    pageSize:10,  //每页数据量
                    RowsTotal:0  ,  //总数据量                
                    dataList:[], //该页数据
                    pageNo:1,    //页数
                },     
               base_url:"http://127.0.0.1:8000",
            page:{
                pageTotal:0, //总页数
                pageSize:10,  //每页数据量
                RowsTotal:0  ,  //总数据量                
                dataList:[], //该页数据
                pageNo:1,    //页数
            },    
      }
    },
    methods: {
            get_photourl(url1){return this.base_url+url1},

    loadBooks (i) {
        /*   加载书籍  */
        this.page.pageNo= i || this.page.pageNo  ;
        this.$axios(
            {
                method:"get",
                url:"http://127.0.0.1:8000/daily_book/?page="+this.page.pageNo+"&page_size="+this.page.pageSize,
                headers:{Authorization:"Bearer"+this.$store.state.token},
            }
        )
        .then(res=>{
            console.log(res.data)
            this.page.dataList=res.data.data;      // 该页数据
            this.page.pageTotal=res.data.pageSum;    // 总页数
            this.page.RowsTotal=res.data.sum;        //总数据量
            this.page.pageSize=res.data.pagesize;    //每页数据
        })
        .catch(err=>{
             console.log(err)
        }) 
    },       

      onSubmit() {
            this.chat=true;
            console.log(this.input)
            let params=new URLSearchParams()
            params.append("screen",this.input.category),
            params.append("search",this.input.name)
            this.$axios(
              {
                method:"get",
                url:"http://127.0.0.1:8000/search_books/",
                headers:{Authorization:"Bearer"+this.$store.state.token},
                params
              }
            )
            .then(res=>{
                console.log(res.data)
                    this.page.dataList=res.data.data;      // 该页数据
                    this.page.pageTotal=res.data.pageSum;    // 总页数
                    this.page.RowsTotal=res.data.sum;        //总数据量
                    this.page.pageSize=res.data.pagesize;    //每页数据
            })
            .catch(err=>{
              console.log(err)
            })
      },
          handlPreview(index,row){
                //console.log(index,row)
                let {href} = this.$router.resolve({
                path: "/book/"+row.fid,//新页面地址
                //query: { id: localStorage.id }//携带的参数
                });

                window.open(href, '_blank');
            }
            

        },
          created(){
        this.loadBooks();
    },


    }
</script>



<style>
</style>