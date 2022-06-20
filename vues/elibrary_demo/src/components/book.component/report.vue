
<template>
<div>
    <br>
    <el-button type="danger"  @click="centerDialogVisible = true" style="float:right;margin-right:150px;">举报</el-button>

    <el-dialog
            title=""
             :visible.sync="centerDialogVisible"
             width="50%"
             :before-close="handleClose" >
            
            <el-form margin-left:50px>
                <fieldset style="width:90%;" >
                <legend>举报表</legend>
                <el-form-item label="书籍名:" size = 'small'>
                    {{this.filename}}
                </el-form-item>                
                <el-form-item label="书籍编号:" size = 'small'>
                    {{this.fileid}}
                </el-form-item>
                <el-form-item label="举报范围:" size = 'small'>
                    <el-input v-model="range" placeholder="违规内容所在页数" />
                </el-form-item>
                <el-form-item label="违规原因:" size = 'small'>
                    <el-input type = "textarea" v-model="reason" placeholder="请输入违规原因..." maxlength="200" :rows="5"></el-input>
                </el-form-item>
                </fieldset>
            </el-form>


            <span slot="footer" class="dialog-footer">
            <el-button @click="centerDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="sendReportInfo">确定举报</el-button>
            </span>
    </el-dialog>

</div>
    
</template>

<script>
  export default {
    props: ['fileid','filename'],
    data() {
      return {
        centerDialogVisible: false,
        reason:"",
        range:"",
      };
    },
    methods: {
          handleClose(done) {
            this.$confirm('确认关闭？')
            .then(_ => {
                done();
             })
            .catch(_ => {});
      },
    
        sendReportInfo(){
            if(this.range!="" && this.reason!=""){
                this.$axios({
                    url:"http://127.0.0.1:8000/report/"+this.fileid+"/"   ,
                    method:"post",
                    headers: {Authorization: "Bearer "+this.$store.state.token},
                    data:{
                        details:this.reason,
                        range:this.range
                    }
                })
                .then(res=>{
                    this.$message("举报信息已提交")
                    console.log(res)
                    
                    this.range="";
                    this.reason="";
                    this.centerDialogVisible = false


                })
                .catch(err=>{
                    console.log(err)
                })
            }
            else{this.$message("举报信息不能为空！")}
        }


    }
  };
</script>