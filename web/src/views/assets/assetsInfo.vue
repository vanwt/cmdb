<template>
    <div class="show">
        <el-tabs tab-position="left" style="height: 100%">
            <el-tab-pane label="资产详情" lazy>
                <info-card :tableData="infoData"></info-card>
            </el-tab-pane>
            <el-tab-pane label="硬件信息" lazy>硬件信息</el-tab-pane>
            <el-tab-pane label="变更记录" lazy>变更记录</el-tab-pane>
            <el-tab-pane label="监控" lazy>监控</el-tab-pane>
            <el-tab-pane label="桌面" lazy>桌面</el-tab-pane>

        </el-tabs>
    </div>
</template>

<script>
  import InfoCard from "@/components/InfoCard";
  import {mapGetters} from 'vuex'

  export default {
    name: "assetsInfo",
    components: {
      InfoCard
    },
    computed: {
      ...mapGetters([
        "getAssetsId"
      ])
    },
    data() {
      return {
        infoData: []
      }
    },
    methods: {
      getAsset() {
        let asset_id = undefined;
        this.getAssetsId.forEach(item => {
          if (item.path === this.$route.path) {
            asset_id = item.id
          }
        });

        this.$http.get(`api/v1/assets/info/${asset_id}/`)
          .then(resp => {
            this.infoData.push(resp.data)
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了:' + err.data.message,
            duration: 0
          });
        })
      },
      clearData() {
        this.infoData = []
      }
    },
    watch: {
      '$route.path': {
        handler(new_v, old_v) {
          this.clearData();
          this.getAsset()
        },
        deep: true,
        immediate: true
      }
    },
  }
</script>

<style scoped>
    .show {
        height: 800px;
    }
</style>