<template>
  <div class="commentPage">



    <div class="star">
      <div style="float:left;">
        <div style="height:40px;">
        <!--高度大小调整      问题：俩个star，只想改一个   -->
          <span>评分:</span>
          <i style="font-size: 35px"><el-rate  v-model="starNum" show-text style="display:inline;"></el-rate></i>
        </div>
      </div>
        <div>
          <el-input
            type="textarea"
            placeholder="请输入评论 . . ."
            v-model="firstComments"
            :rows="4"/>
      <!-- 发布按钮 -->
          <span style="margin-right:1px;float: right;"><el-button @click="submit" type="primary">发表评论</el-button></span>
        </div>


    </div>

<br/><br/>
        <!--评论结果显示-->

        
        <div>
            <el-pagination 
                background
                layout="total,prev, pager, next ,jumper" 
                @current-change="ResetPageNo"
                :current-page="commentsPage.pageNo"
                :page-size="commentsPage.pageSize"
                :total="commentsPage.RowsTotal" >
            </el-pagination> 
        </div>   

<hr>
      <div style="width:100%;margin-top:10px;" v-for="(item,index) in commentsPage.dataList" :key="index">
        <div >
                <!--左边id部分-->
                <div style="float:left;">
                  <span style="margin-left:10px;color:#3D9EEA;font-size:16px;font-weight: bolder;">
                    <strong>{{item.userid}}</strong>
                  </span>
                </div>
                <!--右边显示时间评分等-->
                <div style="float:right">
                    <span style="margin-right:10em;color: grey;">{{item.stime | timeFormat() }}</span>
                    <span style="margin-right:20px;">                  
                      <el-rate v-model="item.grade" disabled  text-color="#ff9900" score-template="{value}" style="display:inline;"></el-rate>
                    </span>
                </div>
                <div style="clear:both;margin:5px 50px;font-size:16px;">{{item.evaluation }}</div>

      </div>
      <hr>
    </div>

  </div>
</template>


<script>
import moment from 'moment'

export default ({
    name:"book_comments",
    //接受的参数
    props: ['bookid'],
    data(){
        return {
        
          starNum:null,
   

            commentsList:[],
            firstComments:"",
            commentsPage:{
                    pageTotal:0, //总页数
                    pageSize:10,  //每页数据量
                    RowsTotal:0  ,  //总数据量                
                    dataList:[], //该页数据
                    pageNo:1,    //页数
                },          




        }
    },

    //过滤器
    filters: {
        timeFormat: function (value) {
            if (!value) return '';
	          return moment(value).format('YYYY-MM-DD hh:mm:ss');
      }
    },
    methods:{

        
        //评论书籍
        submit(){
            let token=this.$store.state.token;
            if(this.starNum>0  && this.firstComments.length>0){
                this.$axios({
                    method:'post',
                    //url地址
				            url: 'http://127.0.0.1:8000/comment/'+this.bookid+'/',
                    headers: {Authorization: "Bearer "+this.$store.state.token},
                    data:{
                      grade:this.starNum,
                      evaluation:this.firstComments
                    }
                 })
                .then(res=>{
                    this.$message("评论成功")
                    //重置评论内容
                    this.starNum=null;
                    this.firstComments="";
                    //刷新评论区列表
                    //this.get_commentsList();
                    this.getPageList()

                 })
                .catch(err=>{
                    this.$message("发生位置错误")
                    console.log(err)
                })
             }
             else{
               this.message("请正确填写内容！！")
             }
        },


            //获取当前页的数据
            getPageList(i){
                var mybookid=this.$route.params.fid;
                this.commentsPage.pageNo= i || this.commentsPage.pageNo  ; 
                //上传文件历史
                this.$axios({
                    method:"get",
                    url: "http://127.0.0.1:8000/comment/"+mybookid+"/?page="+this.commentsPage.pageNo+"&page_size="+this.commentsPage.pageSize,
                    headers: {Authorization: "Bearer "+this.$store.state.token},
                })
                .then(res=>{
                   // alert("获取成功")
                    console.log(res.data)
                    this.commentsPage.dataList=res.data.data;      // 该页数据
                    this.commentsPage.pageTotal=res.data.pageSum;    // 总页数
                    this.commentsPage.RowsTotal=res.data.sum;        //总数据量
                    this.commentsPage.pageSize=res.data.pagesize;    //每页数据

                    //console.log(this.commentsPage.dataList)
                })
                .catch(err=>{
                    console.log(err);
                })

            },


            //修改页数
            ResetPageNo(index){
                this.getPageList(index);
            },


    },

    created(){

      this.getPageList();
      /*
      //初始化评论列表  
      var mybookid=this.$route.params.fid; 
        this.$axios({
                method:'get',
                //url地址
			          url: 'http://127.0.0.1:8000/comment/'+mybookid+'/',
                headers: {Authorization: "Bearer "+this.$store.state.token},
            })

            .then(res=>{
                let datalist=res.data;
                console.log(res);
                console.log(12345)
                this.commentsList=datalist;

            })
            .catch(err=>{
              console.log(err)
                this.$message("发生未知错误")
                alert("获取评论信息时候")
            })
*/
    }

})
</script>


<style scoped>

/* 控制星星大小*/ 
.el-rate  /deep/ .el-rate__icon{
  font-size: 30px;
  margin-right: 0;
}

.commentPage{
  width:70%;
  margin-left:190px;
  float: left;
}

.head {
  background-color: rgb(248, 244, 248);
  position: relative;
  border-radius: 5px;
  padding: 0px;
  margin: 0px;
  height :100%;
  width: 70%;
}

.star{
  height: auto;
  width: 100%;
  margin:0;
  padding:0;
  
}

/* 评论框 */
.head input {
  position: absolute;
  top: 13px;
  left: 80px;
  height: 45px;
  border-radius: 5px;
  outline: none;
  width: 65%;
  font-size: 20px;
  padding: 0 20px;
  border: 2px solid #f8f8f8;
}
/* 发布评论按钮 */
.head button {
  position: absolute;
  top: 13px;
  right: 20px;
  width: 120px;
  height: 48px;
  border: 0;
  border-radius: 5px;
  font-size: 20px;
  font-weight: 500;
  color: #fff;
  background-color: rgb(118, 211, 248);
  cursor: pointer;
  letter-spacing: 2px;
}
/* 鼠标经过字体加粗 */
.head button:hover {
  font-weight: 600;
}


.comment_show{
  width:70%;


}
.list-group-item
{ 
  display: flex;
  position: relative;
  padding: 10px 10px 0px 0;
}

.first-userid{
  color: #504f4f;
}
.first-comment {
  flex: 9;
}
.first-time {
  color: #767575;
}
.first-comment {
  margin-top: 5px;
}
/* 右边分数显示 */
.first-right{
  position: absolute;
  right: 1%;
  top: 10px;
}
.first-right span {
  margin-right: 20px;
  cursor: pointer;
}




.list-group-item{
  display: flex;
  position: relative;
  padding: 10px 10px 0px 0;
}



</style>


