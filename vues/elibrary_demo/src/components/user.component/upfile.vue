<template>
  <div class='myelement' >
    <el-form ref="book1" :model="book1" label-width="130px" :rules="rules"  style="margin-left: 300px;">
<!--     
     <fieldset style="width:40%;" >
        <legend >个人信息</legend>
         姓名 
        <el-form-item label="姓名：" prop="apply_person_name" size = 'small' >
          <el-input v-model="form.apply_person_name" placeholder="请输入姓名"  class="input_width"></el-input>
        </el-form-item>
      </fieldset>-->
      <br>
<!--

      <fieldset style="width:40%;">
        <legend>报名信息</legend>
        <el-form-item label="学校/公司/组织：" prop="apply_company" size = 'small' >
          <el-input v-model="form.apply_company" placeholder="请输入公司名"  class="input_width" ></el-input>
        </el-form-item>

        <el-form-item label="专业/部门：" prop="apply_department" size = 'small' >
          <el-input v-model="form.apply_department" placeholder="请输入部门"  class="input_width"></el-input>
        </el-form-item>

        <el-form-item label="报名赛区：" prop="apply_area" size = 'small'>
          <el-radio v-model="form.apply_area" label="集团内部赛区">集团内部赛区</el-radio>
          <el-radio v-model="form.apply_area" label="社会开放赛区">社会开放赛区</el-radio>
        </el-form-item>

        <el-form-item label="作品方向：" prop="competition_product_target" size = 'small'>
          <el-radio v-model="form.competition_product_target" label="精益生产">精益生产</el-radio>
          <el-radio v-model="form.competition_product_target" label="智慧服务">智慧服务</el-radio>
          <el-radio v-model="form.competition_product_target" label="创新应用">创新应用</el-radio>
        </el-form-item>

        <el-form-item label="团队名称：" prop="team_name" size = 'small' >
          <el-input v-model="form.team_name" placeholder="请输入团队名称"  class="input_width"></el-input>
        </el-form-item>
      </fieldset>-->
      <br>

      <fieldset style="width:40%;" >
        <legend>书籍信息</legend>
        <el-form-item label="书名：" prop="fname" size = 'small' >
          <el-input v-model="book1.fname" placeholder="文件名（必填）"  class="input_width" ></el-input>
        </el-form-item>

        <el-form-item label="所需积分：" prop="f_fees" size = 'small' >
          <el-input-number  v-model="book1.f_fees" placeholder="所需积分（非负整数）"  class="input_width"  
                       :min="0" />
        </el-form-item>

        <el-form-item label="出版社："  size = 'small' >
          <el-input v-model="book1.publisher" placeholder="出版社"  class="input_width" ></el-input>
        </el-form-item>

        <el-form-item label="作者："  size = 'small' >
          <el-input v-model="book1.writer" placeholder="作者"  class="input_width" ></el-input>
        </el-form-item>

        <el-form-item label="IBSN: "  size = 'small' >
          <el-input v-model="book1.ISBN_num" placeholder="IBSN码"  class="input_width" ></el-input>
        </el-form-item>

        <!-- 上传的文件 -->
        <el-form-item ref="upload_attach_item"  label="作品书籍：" prop="file" size = 'small' >
          
          <el-upload
            ref="upload_attach"
            class="upload-demo"
            name="file"   
            action="http://127.0.0.1:8000/books/"
            multiple
            :headers="headers"
            
            :limit="1"
            :on-change="changFile"
            :on-exceed="handleExceed"
            :on-remove="removeFile"
            :file-list="fileList"
            :auto-upload="false"
            :http-request="uploadSectionFile">


            
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            
          </el-upload>
          <el-progress :percentage="progressPercent" v-show="show_progress"></el-progress>

        </el-form-item>
<br>

    <el-form-item     label="类别：">
            <el-checkbox-group  v-model="book1.category">
              <el-checkbox v-for="(it,index) in check_Items" :label="it.label" :key="index">{{it.label}}</el-checkbox>
            </el-checkbox-group>
     </el-form-item>

        <el-form-item label="书籍内容：" prop="content" size = 'small' >
          <el-input type = "textarea" v-model="book1.content" placeholder="书籍内容简介"
                    maxlength="200" show-word-limit class="input_width" :rows="5" ></el-input>
        </el-form-item>
        <div slot="tip" class="el-upload__tip" style="margin-left:30px">注:请正确填写书籍信息</div>

              <br>
        <div style="text-align:right;margin-right: 100px;">
          <el-button type="primary" v-on:click="onSubmit('book1')">提交</el-button>
        </div>
      </fieldset>
      <br>


    </el-form>

  </div>
</template>

<script>
import loading from './loading';
  export default {
    name: 'file_upload',
    data () {
      //复选框的选项
        const check_Items=[
          { key:1,label:"数学"},
          { key:2,label:"物理"},
          {key:3,label:"化学"},
          {key:4,label:"文学"},
          {key:5,label:"外语"},
          {key:6,label:"计算机"},
          {key:7,label:"生物"}
        ]
      //验证密码

      var validateAttach = (rule, value, callback) => {

        console.log(this.fileList.length)
        if (this.fileList.length == 0) {
          callback(new Error('请选择附件'));
        } else {
          callback();
        }
      };


      return {
        //token
        headers:{Authorization: "Bearer "+this.$store.state.token},
       // validateAttach,
     
        //复选框的选项
        check_Items,

        book1:{
          fname:"",
          f_fees:0,
          writer:"",
          ISBN_num:"",
          publisher:"",
          content:"",
          file:null,
          category:[],
        },
        fileList:[],
        progressPercent:0,
        show_progress:false,
        //强制要求
        rules: {
          fname: [
            { required: true, message: '请输入文件名', trigger: 'blur'},
          ],
          f_fees: [
            { required: true, message: '输入积分不能为空', trigger: 'blur' },
          ],
          content: [
            { required: true, message: '请输入内容简介', trigger: 'blur' },
          ],
          file: [
            // { required: true, message: '请输入选择参赛作品', trigger: 'blur' },
            { validator: validateAttach }
          ],

        },
      }
    },
    methods: {
      changFile(file, fileList) {
       // console.log("changFile");
       // console.log(fileList);
        //选择文件后，给fileList对象赋值
        this.fileList = fileList
        this.$refs.upload_attach_item.validate();

      },
      removeFile(file, fileList){
        this.fileList = fileList
        this.$refs.upload_attach_item.validate();
      },
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制最多选择 1 个文件`);
      },
  
      setClear(){
        this.book1.fname="";
        this.book1.f_fees=0;
        this.book1.writer="";
        this.book1.ISBN_num="";
        this.book1.publisher="";
        this.book1.content="";
        this.book1.file=null;
        this.book1.category=[];
      },

      onSubmit(formName) {
        // 校验合法性
        this.$refs[formName].validate((valid) => {
          if (valid) {
            // alert('发送post请求!');
            console.log('submit!')
            console.log(this.book1)
            this.$refs.upload_attach.submit() // 触发调用uploadSectionFile，拿到param参数里面的File
          } else {
            console.log('error submit!!');
            this.$message({
              message: '请填写完整信息再后提交',
              type: 'error'
            });
            return false;
          }

        });

        // this.apply();
        // this.$refs.upload_attach.submit() // 触发调用uploadSectionFile，拿到param参数里面的File

      },

      //自定义http请求
      uploadSectionFile(param) {
        //console.log(param)

      console.log(this.book1.category)

        let formdata = new FormData();

        // todo 非常重要，一定要加file.raw，从浏览器中查看需要使用binary类型，后台才能正确接收
        // this.form.files = this.fileList[0].raw
        // console.log(this.fileList[0].raw)
/*------------------------------------------------------------------------------------ */
        this.book1.file = param.file // 将form中的files字段赋值File对象
       // console.log(param.file)

      formdata.append("fname",this.book1.fname);
      formdata.append("f_fees",this.book1.f_fees);
      formdata.append("writer",this.book1.writer);
      formdata.append("ISBN_num",this.book1.ISBN_num);
      formdata.append("publisher",this.book1.publisher);
      formdata.append("content",this.book1.content);
      formdata.append("file",this.book1.file);
      formdata.append("category",this.book1.category);
      //data.append("",this.book1.);
      //data.append("",this.book1.);

      

//console.log("fname=:.+.+.+.+.+.+.+.+.+.");
//console.log(data.get("fname"));
        // 将form表单中的值都赋值给FormData传递给后台
 /*       for(let key in this.book1){
          data.append(key,this.book1[key])
        }
*/
    //   console.log(data);
        const _loading = loading(`作品上传中，请稍后...`)

        // this.show_progress = true
        const config = {
          onUploadProgress: progressEvent => {
            // progressEvent.loaded:已上传文件大小
            // progressEvent.total:被上传文件的总大小
            this.progressPercent = Number((progressEvent.loaded / progressEvent.total * 100).toFixed(0))
            _loading.setText('作品上传中')
           // _loading.setText('作品上传中，进度：' + this.progressPercent + "%") //更新dialog进度，优化体验
            
           // console.log(this.progressPercent)
          },
          headers: {
            Authorization: "Bearer "+this.$store.state.token ,           
            'Content-Type': 'multipart/form-data'
          }
        }
//发送   //必须是anction？
//-------------------------------------------------------------------------
//console.log("-----------------------")
//console.log(param.action);
//console.log(formdata);
//console.log(config);
//console.log("-------------------------------------");
 /*       this.$axios
          .post(param.action,formdata,config)
          .then(resp => {
            console.log('请求本地接口OK')
            console.log(resp)
            this.fileList = [];// 提交完成清空附件列表
            _loading.close(); // 关闭加载框
            // this.show_progress = false
            this.progressPercent = 0


            if(resp.data.code == -1){
              // 接口返回-1，就是报名失败，提示消息提示用户
              this.$message({
                message: resp.data.msg,
                type: 'error'
              });
            } else if(resp.data.code == 0){
              console.log(resp.data)
              //报名成功
              this.$message({
                message: "报名成功",
                type: 'success'
              });

              // 跳转到主页面
              // this.$router.replace('/home')

            }

          })
          .catch(function (error) { // 请求失败处理
           _loading.close(); // 关闭加载框
            console.log('请求本地接口失败' + error);
          });*/

          this.$axios({
            method:"post",
            url: 'http://127.0.0.1:8000/books/',
            data:formdata,
            headers: {
            Authorization: "Bearer "+this.$store.state.token ,           
            "Content-Type": 'multipart/form-data'
            },
            contentType:false,
            processData:false,
          })
          .then(res=>{
            this.$message("上传成功")
            console.log(res)
            this.fileList = [];// 提交完成清空附件列表
            _loading.close(); // 关闭加载框
            // this.show_progress = false
            this.progressPercent = 0
            this.setClear()
          })
          .catch(function (error) { // 请求失败处理
           _loading.close(); // 关闭加载框
            console.log('请求本地接口失败' + error);
          });


      },validateAttach (rule, value, callback) {
        console.log(value)
        console.log(this.$refs.upload_attach)

      },

    },
    created () {
    },
  }
</script>

<style scoped>
  .myelement {
    text-align:center;
    width:100%;
  }
  .input_width{
    width: 50%;
    width: 300px;
  }
  fieldset {
    border:2px solid #DCDFE6;  text-align:left; border-radius: 8px;
  }
</style>

