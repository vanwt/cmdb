<template>
    <div class="box">
        <h1>您没有访问此URL的权限...</h1>
        <hr>
        <el-image :src="src"></el-image>
        <hr>
        <el-button type="success" @click="goHome">返回首页</el-button>
    </div>

</template>

<script>
  export default {
    name: "Forbidden",
    methods: {
      goHome() {
        window.location.href = '/home'
      }
    },
    data() {
      return {
        src: require("@/assets/image/403.jpg")
      }
    }
  }
</script>

<style scoped>
    html, body {
        padding: 0;
        margin: 0;
        height: 100%;
        width: 100%;
    }

    .box {
        padding-top: 100px;
        width: 100%;
        height: 100%;
        background-color: rgba(252, 255, 204, 0.79);
        text-align: center; /*文本水平居中*/
    }
</style>