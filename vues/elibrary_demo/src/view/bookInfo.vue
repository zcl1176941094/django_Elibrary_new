<template>
    <div class="book">
        <!--书籍信息-->
        <div  class="bookInformation">
            <el-form style="width:70%;">
            <fieldset style="width:100%;margin: auto;" >
                <legend>书籍信息</legend>
                <div style="float:left;margin-left:100px;"><el-image :src="this.bookInfo.file_photo"   class="book-avator"/></div>
                    
                    <h2><strong>{{bookInfo.fname}}</strong></h2>
                    <br/>
                    <span>类别: </span><span v-for="i in this.bookInfo.category">{{i}} </span> &ensp; &ensp;
                    <span>评分： {{this.bookInfo.ave_score}}</span>                    
                    <br/>
                    <span>IBSN : {{this.bookInfo.IBSN_num}}</span> &ensp; &ensp;
                    <span>  出版社:{{this.bookInfo.publish_er}}</span>
                    <br/>
                    <span> 上传人：{{this.bookInfo.uploader}}</span>
                    <br/>
                    <div>
                    <span>内容: {{this.bookInfo.content}}</span>
                    </div>
                  
                    <span>收藏次数: {{this.bookInfo.collection_times}}</span> 
                    <span>下载次数: {{this.bookInfo.download_times}}</span>
                    <span>评论次数: {{this.bookInfo.comment_times}}</span>
<!--
                <el-form-item>
                    <button>1231</button>
                    <el-button type="warning" icon="el-icon-Star" >收藏</el-button>
                    <el-button type="info" icon="el-icon-Download" >下载</el-button>
                </el-form-item>
-->
            </fieldset>
            </el-form>


            
        </div>
<br><br>
<!--pdf书籍预览-->
        <div>
            <pdf_test :pdfurl="this.bookInfo.file" :isvalid1="this.bookInfo.is_valid" :filename="this.bookInfo.fname"></pdf_test>
        </div>

<!--举报窗口-->
        <div>
            <report_test :fileid="this.bookInfo.fid" :filename="this.bookInfo.fname"></report_test>
        </div>


<br><br><br>
        <!--评论-->
        <div class="bookComments">
            <!--传参数给子组件-->
            <comment :bookid="bookInfo.fid"></comment>
        </div>


</div>

</template>



<script>
import  pdf_test from "../components/book.component/pdf_test.vue"
import report_test from "../components/book.component/report.vue"
import comment from '../components/book.component/comment.vue'
//vue找本地图片是找不到的 所以需要用到 require（）

export default {
  
    //应为路由传参操作,传入fid
    name:"file_Info",
    components: { comment,pdf_test,report_test },
    data(){
     
        return{
               //params方式路由传参
            newfid:this.$route.params.fid,
            isDisabled:false,
            //书籍信息
            bookInfo:{
                fid:0,
                fname:"",
                ave_score:0.0,

                category:"",
                content:"",
                f_fees:0,
                file:"",                
                file_photo:"",
                publish_er:"",
                IBSN_num:"",
                uploader:"",
                comment_times:0,
                download_times:0,
                collection_times:0,
                is_valid:true,
            },
         

        }
    },

    created(){
        //初始化获得书籍信息
        this.get_fileInfo();
    },


    methods:{
        get_fileInfo(){
            this.$axios({
                method:"get",
                url:"http://127.0.0.1:8000/book_get/"+this.newfid+"/",
                headers: {Authorization: "Bearer "+this.$store.state.token},
            })
            .then(res=>{
                let data=res.data;

                this.bookInfo.fid=data.fid;
                this.bookInfo.fname=data.fname;
                this.bookInfo.ave_score=data.ave_score;
                this.bookInfo.category=data.category;
                this.bookInfo.content=data.content;
                this.bookInfo.f_fees=data.f_fees;
                this.bookInfo.file=data.file;
                this.bookInfo.file_photo=data.file_photo;
                this.bookInfo.publish_er=data.publish_er;
                this.bookInfo.IBSN_num=data.IBSN_num;
                this.bookInfo.uploader=data.uploader;
                this.bookInfo.comment_times=data.comment_times;
                this.bookInfo.download_times=data.download_times;
                this.bookInfo.collection_times=data.collection_times;
                this.bookInfo.is_valid=data.isvalid;

                this.isDisabld=data.is_valid;
            })
            .catch(err=>{
                console.log(err)
            })
        }
    },


}
</script>



<style  scoped="scoped">

.book{

}

.bookInformation{
    width: 100%;
    height:30%;
    background-color: rgb(255, 255, 255);
    padding-left: 50px;
    padding-right: 50px;
    display:flex;
    justify-content:center;
}

.bookComments{
    margin:0;
    padding:0;
    display:flex;
    justify-content:center;
}

.book-avator {
    margin-left: 20px;
    float:left;
    width:210px;
}

</style>
