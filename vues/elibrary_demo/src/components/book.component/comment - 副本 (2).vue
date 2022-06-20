<template>
  <div class="commentPage">



    <div class="star">
        <div >
          <span>评分:</span>
          <img v-for="(star,index) in stars" v-bind:src="star.src" width="30px" height="30px" v-on:click="rating(index)"/>
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
                    <span style="margin-right:20px;">{{ item.grade }}分</span>
                </div>
                <div style="clear:both;margin:5px 50px;font-size:16px;">{{item.evaluation }}</div>

      </div>
      <hr>
    </div>

  </div>
</template>


<script>
import moment from 'moment'
//vue找本地图片是找不到的 所以需要用到 require（）
var starOffImg = require('./star_off.jpg');
var starOnImg = require('./star_on.png');
export default ({
    name:"book_comments",
    //接受的参数
    props: ['bookid'],
    data(){
        return {
        
          starNum:0,
        stars:[{
          src:starOffImg,   
          active:false  //这个是在这最后计算总数的时候需要用到
        },{
          src:starOffImg,
          active:false
        },{
          src:starOffImg,
          active:false
        },{
          src:starOffImg,
          active:false
        },{
          src:starOffImg,
          active:false
          }],

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
      /*
        //获取书籍评论信息
        get_commentsList(){
            //this.commentsList=[];
            var mybookid=this.$route.params.fid;
            this.$axios({
                method:'get',
                //url地址
			          url: 'http://127.0.0.1:8000/comment/'+mybookid+'/',
                headers: {Authorization: "Bearer "+this.$store.state.token},
            })

            .then(res=>{

                let datalist=res.data;
                console.log(res.data);
                console.log(12345)
                this.commentsList=datalist;

            })
            .catch(err=>{
              console.log(err)
                this.$message("发生未知错误")
                alert("获取评论信息时候")
            })

        },*/
        
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
                    this.starNum=0;
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

    //这个方法是点击图片的时候才会掉  并不是一进页面就会走这个方法
    rating(index){
      var total = this.stars.length;//星星总数量
      var idx = index+1;//index 代表点击星星的下标  +1是因为下标是从0开始计数的  - idx代表要显示多少克星星

      //如果if=0说明是初始化状态
      if(this.starNum === 0){
        this.starNum = idx;
        for (var i=0; i < idx; i++){
          this.stars[i].src = starOnImg;
          this.stars[i].active = true;
        }
      }else{
      //  如果再次点击当前选中的星级-仅取消掉当前星级,保留之前的。（比如我点击了第三颗星星它会亮起前三颗星星，当我再点击第三颗星的时候回灭掉第三颗星，前两颗仍是亮着的）
        if(idx == this.starNum){  //如果点亮的星和上一次的一样
          for (var i = index; i< total; i++){ //他会从点击的那个下标开始循环(是点亮那颗的下标作为基数，而不是 我们+1的idx)
              this.stars[i].src = starOffImg; //然后关掉此下标开始后面的星
              this.stars[i].active = false;
          }
        }

        //如果小于当前最高星级，则直接保留当前星级
        if(idx < this.starNum){
          for (var i = idx; i<this.starNum; i++){
            this.stars[i].src = starOffImg;
            this.stars[i].active = false;
          }
        }

        //如果大于当前星级，则直接选到该星级
        if(idx > this.starNum){
          for(var i = 0; i < idx; i++){
            this.stars[i].src = starOnImg;
            this.stars[i].active = true;
          }
        }

        //计算器统计当前的星星数量
        var count = 0;
        for(var i = 0; i < total; i++){
          if (this.stars[i].active){
              count++;
          }
        }
        this.starNum = count;
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


