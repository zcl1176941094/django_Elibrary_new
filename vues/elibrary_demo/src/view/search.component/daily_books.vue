<template>
  <div style="align:center;margin-left:auto;margin-right: auto;">
  <!--日常推荐书籍-->
  <div >
    <el-row   type="flex" justify="center">

      <el-tooltip effect="dark" placement="right"
                  v-for="(item,index) in page.dataList.slice(0,5)"
                  :key="index">
        <!-- slot="content" 鼠标放置显示的内容  -->
        <p slot="content" style="font-size: 14px;margin-bottom: 6px;">{{item.fname}}</p>
        <p slot="content" style="font-size: 13px;margin-bottom: 6px">
          <span>{{item.writer}}</span> /
          <span>{{item.publisher}}</span> /
          <span>{{item.category}}</span>
        </p>
        <p slot="content" style="width: 300px" class="abstract">{{item.content}}</p>
        <el-card style="width: 135px;margin-bottom: 20px;height: 233px;float: left;margin-right: 15px" class="book"
                 bodyStyle="padding:10px" shadow="hover">
          <div class="cover">
            <img :src="get_photourl(item.file_photo)" alt="封面">
          </div>
          <!--   书籍内容下方的显示    -->
          <div class="info">
            <div class="title">
                <el-link :href="get_bookurl(item.fid)" target="_blank">{{item.fname}}</el-link>
            </div>
          </div>
          <div class="author">{{item.writer}}</div>
        </el-card>
      </el-tooltip>
    </el-row>
<!--------------------------------------------------------->
    <el-row type="flex" justify="center">

      <el-tooltip effect="dark" placement="right"
                  v-for="(item,index) in page.dataList.slice(5,10)"
                  :key="index">
        <!-- slot="content" 鼠标放置显示的内容  -->
        <p slot="content" style="font-size: 14px;margin-bottom: 6px;">{{item.title}}</p>
        <p slot="content" style="font-size: 13px;margin-bottom: 6px">
          <span>{{item.writer}}</span> /
          <span>{{item.publisher}}</span> /
          <span>{{item.category}}</span>
        </p>
        <p slot="content" style="width: 300px" class="abstract">{{item.content}}</p>
        <el-card style="width: 135px;margin-bottom: 20px;height: 233px;float: left;margin-right: 15px;" class="book"
                 bodyStyle="padding:10px" shadow="hover">
          <div class="cover">
            <img :src="get_photourl(item.file_photo)" alt="封面">
          </div>
          <!--   书籍内容下方的显示    -->
          <div class="info">
            <div class="title">
                <el-link :href="get_bookurl(item.fid)" target="_blank">{{item.fname}}</el-link>
            </div>
          </div>
          <div class="author">{{item.writer}}</div>
        </el-card>
      </el-tooltip>
    </el-row>
  </div>
    <el-row>
        <el-pagination 
            small background
            layout="total,prev, pager, next " 
            @current-change="ResetPageNo"
            :current-page="page.pageNo"
            :page-size="page.pageSize"
            :total="page.RowsTotal" >
        </el-pagination> 
    </el-row>
  </div>
</template>

<script>

  export default {
    name: 'Books',

    data () {
      return {
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

    get_bookurl(bookid){return "http://localhost:8080/#/book/"+bookid},

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



            //修改页数
            ResetPageNo(index){
                this.loadBooks(index);
            },
   
    },

    created(){
        this.loadBooks();
    },





  }
</script>


<style scoped>

  .cover {
    width: 115px;
    height: 172px;
    margin-bottom: 7px;
    overflow: hidden;
    cursor: pointer;
  }

  img {
    width: 115px;
    height: 172px;
    /*margin: 0 auto;*/
  }

  .title {
    font-size: 14px;
    text-align: left;
  }

  .author {
    color: #333;
    width: 102px;
    font-size: 13px;
    margin-bottom: 6px;
    text-align: left;
  }

  .abstract {
    display: block;
    line-height: 17px;
  }

  .el-icon-delete {
    cursor: pointer;
    float: right;
  }

  .switch {
    display: flex;
    position: absolute;
    left: 780px;
    top: 25px;
  }

  a {
    text-decoration: none;
  }

  a:link, a:visited, a:focus {
    color: #3377aa;
  }

</style>
