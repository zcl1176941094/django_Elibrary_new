<template>
    <div>
  <span>Stars测评:{{starNum}}颗</span>
  <div>
    <img v-for="(star,index) in stars" v-bind:src="star.src" width="20px" height="20px" v-on:click="rating(index)"/>
  </div>
</div>

</template>


<script>
//vue找本地图片是找不到的 所以需要用到 require（）
var starOffImg = require('./star_off.jpg');
var starOnImg = require('./star_on.png');
export default {
    name: "Evaluation",
  data(){
      return{
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
        }]
      }
  },
  methods:{
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
    }
  }
}

</script>





<style scoped>




</style>