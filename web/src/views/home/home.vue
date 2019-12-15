<template>
    <el-row class="home" :gutter="20">
        <el-col :span="24">
            <div class="num">
                <el-card shadow="hover" :body-style="{display:'flex', padding:0}">
                    <i class="icon el-icon-s-platform" style="background:#199bcc"></i>
                    <div class="detail">
                        <p class="num">{{vm}}</p>
                        <p class="txt">虚拟机</p>
                    </div>
                </el-card>
                <el-card shadow="hover" :body-style="{display:'flex', padding:0}">
                    <i class="icon el-icon-s-platform" style="background:#59c906"></i>
                    <div class="detail">
                        <p class="num">{{server}}</p>
                        <p class="txt">物理机</p>
                    </div>
                </el-card>
                <el-card shadow="hover" :body-style="{display:'flex', padding:0}">
                    <i class="icon el-icon-s-platform" style="background:#c9c91c"></i>
                    <div class="detail">
                        <p class="num">{{server + vm}}</p>
                        <p class="txt">全部主机</p>
                    </div>
                </el-card>
                <el-card shadow="hover" :body-style="{display:'flex', padding:0}">
                    <i class="icon el-icon-s-platform" style="background:#c9c91c"></i>
                    <div class="detail">
                        <p class="num">1</p>
                        <p class="txt">用户数</p>
                    </div>
                </el-card>
            </div>
            <div class="graph">
                <el-card shadow="hover">
                    <div style="height: 615px;">
                        <el-calendar :value="new Date()">
                        </el-calendar>

                    </div>
                </el-card>
                <el-card shadow="hover">
                    <div style="height: 260px;"></div>
                </el-card>
            </div>
        </el-col>
    </el-row>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    name: "Home",
    computed: {
      ...mapGetters([
        "getUser"
      ])
    },
    data() {
      return {
        url: require("@/assets/image/avatar.jpg"),
        server: 0,
        vm: 0,
      }
    },
    methods: {
      test() {
        this.$http.get("api/v1/user/test/")
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            console.log("成功")
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了:获取信虚拟机息失败',
            duration: 0
          });
        })
      },
      getAssetsData() {
        this.$http.get("api/v1/assets/server-count/")
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.server = resp.data.num
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了:获取物理机信息失败',
            duration: 0
          });
        });
        this.$http.get("api/v1/assets/vm-count/")
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.vm = resp.data.num
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了:获取信虚拟机息失败',
            duration: 0
          });
        })
      }
    },
    created() {
      this.getAssetsData()
    }
  }
</script>

<style lang="scss" scoped>
    @import '~@/assets/scss/home.scss';
</style>