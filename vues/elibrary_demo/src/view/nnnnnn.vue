<template>
  <el-menu class="el-menu-vertical-demo" :collapse="isCollapsed" background-color="#545c64" :default-active='activeIndex' text-color="#fff" active-text-color="#7EA8F5">
    <section v-for="(item,index) in addRouters" :key="item.name" :class="isCollapsed ? 'collapsed':''">
      <!-- 有子菜单 -->
      <el-submenu :index=" `${index+1}`" v-if="!item.meta.hidden && item.children && item.children.length">
        <template slot="title">
          <i :class="`icon iconfont ${item.meta.icon}`"></i>
          <span slot="title">{{item.meta.title}}</span>
        </template>
        <section v-for="(item2,index2) in item.children" :key="item2.name">
          <!-- 二级菜单有子菜单 -->
          <el-submenu :index="`${index+1}-${index2+1}`" v-if="item2.children && item2.children.length" class="sub2">
            <template slot="title">
              <span slot="title">{{item2.meta.title}}</span>
            </template>
            <!-- 三级菜单 -->
            <el-menu-item v-for="(item3,index3) in item2.children" v-if="!item3.meta.hidden" :index="item3.name" :key="index3" @click.native="$router.push({name:item3.name})">
              <span slot="title">{{item3.meta.title}}</span>
            </el-menu-item>
          </el-submenu>
          <!-- 二级菜单无子菜单 -->
          <!-- 不是隐藏的，详情页隐藏 -->
          <el-menu-item :index="item2.name" v-else-if="!item2.meta.hidden" @click.native="$router.push({name:item2.name})">
            <span slot="title">{{item2.meta.title}}</span>
          </el-menu-item>
        </section>
      </el-submenu>
      <!-- 无子菜单 -->
      <el-menu-item v-else-if="item.meta.hidden && item.children && item.children.length" :index="item.children[0].name" @click.native="$router.push({name:item.children[0].name})" class="item">
        <i :class="`iconfont ${item.children[0].meta.icon}`"></i>
        <span slot="title">{{item.children[0].meta.title}}</span>
      </el-menu-item>
    </section>
  </el-menu>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    isCollapsed: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters(['addRouters']),
    activeIndex () { //集火的菜单
      return this.$route.name
    }
  }
}
</script>


<style lang="scss" scoped>
section {
  /deep/ .el-submenu__title {
    .icon {
      margin-right: 10px;
    }
    i {
      color: white;
      font-size: 14px;
    }
  }
  /deep/ .el-menu-item {
    padding-left: 50px !important;
  }
  /deep/ .el-menu-item.item {
    padding-left: 19px !important;
    i {
      color: white;
      font-size: 14px;
      margin-right: 12px;
    }
  }
  /deep/ .el-submenu .el-menu-item {
    min-width: 0;
  }
  /deep/ .el-submenu.sub2 .el-submenu__title {
    padding-left: 50px !important;
    i {
      margin-right: 0px;
    }
  }
  /*   /deep/ .el-submenu.sub2 .el-menu-item {
    text-indent: 12px;
  } */
}
.collapsed {
  width: 50px;
  /deep/ .el-submenu__title {
    .el-icon-arrow-right {
      display: none;
    }
    span[slot="title"] {
      display: none;
    }
  }
}
</style>
