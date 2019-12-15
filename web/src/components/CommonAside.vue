<template>
    <el-menu :collapse="getCollapse"
             default-active="2"
             background-color="#304156"
             text-color="#fff"
             active-text-color="#fff"
             class="el-menu-vertical-demo">
        <h3 class="head" v-show="!getCollapse">CMDB-Manager</h3>
        <h3 class="head" v-show="getCollapse">CM</h3>
        <el-menu-item :index="item.path" @click="clickMenu(item)" v-for="item in noChildren" :key="item.name">
            <i :class="'el-icon-'+item.icon"></i>
            <span slot="title">{{item.label}}</span>
        </el-menu-item>

        <el-submenu :index="'1-'+index" v-for="(item,index) in hasChildren" :key="index">
            <template slot="title">
                <i :class="'el-icon-'+item.icon"></i>
                <span>{{item.label}}</span>
            </template>

            <el-menu-item @click="clickMenu(child)" :index="child.name" v-for="child in item.children"
                          :key="child.name">
                <i :class="'el-icon-'+child.icon"></i>
                {{child.label}}
            </el-menu-item>
        </el-submenu>
    </el-menu>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    name: "CommonAside",
    computed: {
      ...mapGetters([
        "getMenu", "getCollapse"
      ]),
      noChildren() {
        return this.getMenu.filter(item => !item.children)
      },
      hasChildren() {
        return this.getMenu.filter(item => item.children)
      },
    },
    methods: {
      clickMenu(item) {
        if(this.$route.name !== item.name){
          this.$router.push({name: item.name});
          this.$store.dispatch("setItem", item)
        }
      }
    }
  }
</script>

<style scoped>
    .el-menu {
        height: 100%;
        border: none;
    }

    .el-menu-vertical-demo:not(.el-menu--collapse) {
        width: 200px;
        min-height: 400px;
    }

    .head {
        text-align: center;
        font-size: 24px;
        color: #fff;
        height: 56px;
        line-height: 56px;
    }
</style>