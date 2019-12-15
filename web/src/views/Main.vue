<template>
    <el-container style="height: 100%">
        <el-aside width="auto"><common-aside></common-aside>
        </el-aside>
        <el-container>
            <el-header><common-header></common-header></el-header>
            <common-tab></common-tab>
            <el-main>
                <router-view />
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
  import CommonHeader from '../components/CommonHeader'
  import CommonAside from '../components/CommonAside'
  import CommonTab from "../components/CommonTab";
  export default {
    name: "Main",
    components: {
      CommonHeader, CommonAside,CommonTab
    }
  }
</script>

<style scoped>
    .el-header{
        background-color: #ffffff;
        border-bottom: 1px solid #e2e2e2;
        width:100%;
    }
    .el-main{
        margin-top: 10px;
        border-top: 1px solid #e2e2e2;
        padding-top: 10px;
    }
</style>