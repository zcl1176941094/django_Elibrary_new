<template>
    <div>
        <el-row>
            
            <el-button @click="downfile" type="info" icon="el-icon-Download" style="float:right;margin-right:150px;" :disabled="!isvalid1">下载</el-button>  
            <el-button  @click="collectfile" type="warning" icon="el-icon-Star" style="float:right;margin-right:40px;" :disabled="!isvalid1">收藏</el-button>                     
            <el-button @click="onPreview" type="primary" icon="el-icon-search" style="float:right;margin-right:40px;" :disabled="!isvalid1">预览</el-button>


        </el-row>
        <el-dialog title="文件预览" :visible.sync="viewVisible" center width="60%" @close='closePreview'>
            <el-row :gutter="20">
                <span>共{{pageCount}}页， 当前第 {{pdfPage}} 页 </span>
                <el-button type="text" size="mini" @click.stop="previousPage">上一页</el-button>
                <el-button type="text" size="mini" @click.stop="nextPage">下一页</el-button>
              
            </el-row>
            <div>
                <pdf :src="src" :page="pdfPage" @num-pages="pageCount = $event" @page-loaded="pdfPage = $event" style="display: inline-block; width: 100%"></pdf>
            </div>
        </el-dialog>
    </div>
</template>
<script>
import pdf from 'vue-pdf'

export default {
    props: ['pdfurl','isvalid1','filename'],
    components:{
        pdf
    },
    data(){
        return {
            viewVisible: false,
            src: null,
            pdfPage : 1,
            pageCount: 0,
            
        }
    },
    methods:{
        onPreview(){
            this.src = pdf.createLoadingTask({
                url: this.pdfurl,
                //httpHeaders: {Authorization:'Bearer '+ this.token}
            });
            this.src.promise.then(pdf => {
                this.viewVisible = true;
            });
        },
        closePreview(){
            this.pdfPage = 1;
        },
        previousPage(){
            let p = this.pdfPage
            p = p > 1 ? p-1 : this.pageCount
            this.pdfPage = p
        },
        nextPage(){
            let p = this.pdfPage
            p = p < this.pageCount ? p+1 : 1
            this.pdfPage = p
        },


        //收藏文件
        collectfile(){
            var mybookid=this.$route.params.fid; 
            this.$axios({
                method:"get",
                url:"http://127.0.0.1:8000/collection/"+mybookid+"/",
                headers: {Authorization: "Bearer "+this.$store.state.token},
            })
            .then(res=>{
                //console.log(res)
                this.$message(res.data.msg)
            })
            .catch(err=>{
                console.log(err)
            })
        },
        //下载文件
        downfile(){
             // window.location = this.pdfurl;
            /*
            let link = document.createElement('a')
            link.href = window.URL.createObjectURL(new Blob([response.data]))
            link.target = '_blank'
            let filename = response.headers['content-disposition']
            link.download = decodeURI(filename)  // 下载的文件名称
            document.body.appendChild(link)  // 添加创建的 a 标签 dom节点
            link.click()  // 下载
            document.body.removeChild(link)  // 移除节点*/
            var mybookid=this.$route.params.fid; 

            this.$axios({
                methods:"get",
                url:"http://127.0.0.1:8000/book_get/"+mybookid+"/download/",
                headers: {Authorization: "Bearer "+this.$store.state.token},
                responseType: 'blob',
            })
            .then(res=>{
                console.log(res)
               /* const blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
                const url = window.URL.createObjectURL(blob)
                window.open(url, '_blank')*/
        let url = window.URL.createObjectURL(new Blob([res.data]))
		let link = document.createElement('a')
		link.style.display = 'none'
		link.href = url;
        //console.log(typeof this.pdfurl)
        var fileName = this.pdfurl.lastIndexOf(".");//取到文件名开始到最后一个点的长度
		let fileNameLength = this.pdfurl.length;//取到文件名长度
		let fileFormat = this.pdfurl.substring(fileName + 1, fileNameLength);//截取文件的后缀名。
        //console.log(this.fileName)
        let newname=this.filename+"."+fileFormat;
        //console.log(newname)
        //为下载文件命 名.pdf
		link.setAttribute('download', newname)
		document.body.appendChild(link)
		link.click()


            })
            .catch(err=>{
                if('msg' in err){
                    this.$message(err)
                }

                console.log(err)
            })
        }
    }
}
</script>   


<style scoped>


    
.button_set{
    float:right;
    margin-left:150px;
}

</style>
