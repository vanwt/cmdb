<template>
    <header>
        <div class="l-content">
            <el-button type="text" @click="switchAside" >
                <i class="el-icon-s-fold" v-if="!getCollapse"></i>
                <i class="el-icon-s-unfold" 
                v-if="getCollapse"></i>
            </el-button>
            <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="$route.path !== '/' ? { path:'/' } : ''">主页</el-breadcrumb-item>
                <el-breadcrumb-item v-if="getMenuItem">{{getMenuItem.label}}
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="r-content">
            <!--            <el-dropdown trigger="click">-->
            <span class="span">
                    <i class="el-icon-user"></i>
                    {{getUser.realname}}
                </span>
            <el-button type="text" style="margin-left: 20px;" class="span" icon="el-icon-s-promotion" @click="logout">
                退出登录
            </el-button>
            <!--                <el-dropdown-menu slot="dropdown">-->
            <!--                    <el-dropdown-item>个人中心</el-dropdown-item>-->
            <!--                    <el-dropdown-item @click.native="logout">退出登录</el-dropdown-item>-->
            <!--                </el-dropdown-menu>-->
            <!--            </el-dropdown>-->
        </div>
    </header>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    name: "CommonHeader",
    computed: {
      ...mapGetters([
        "getMenuItem", "getCollapse", "getUser"
      ])
    },
    methods: {
      switchAside() {
        this.$store.commit("setCollapse")
      },
      logout() {
        this.$confirm('确定要退出系统?', '登出', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$store.commit("clearToken");
          this.$store.commit("clearMenu");
          this.$store.commit("clearUser");
          location.reload()
        }).catch(() => {})
      }
    }
  }
</script>

<style scoped>
    header {
        display: flex;
        height: 100%;
        align-items: center;
        justify-content: space-between;
    }

    .l-content {
        display: flex;
        align-items: center;
    }

    .el-button {
        margin-right: 20px;
    }

    .user {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
</style>
