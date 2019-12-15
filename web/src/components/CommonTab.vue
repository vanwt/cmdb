<template>
    <div class="tab">
        <el-tag :key="tag.label" v-for="tag in getTabs" :closable="tag.name !== 'home'" :disable-transitions="false"
                @close="handleClose(tag)" size="small" type="success"
                @click="changeMenu(tag)"
                :effect="$route.name === tag.name ? 'dark' : 'plain'">
            {{tag.label}}
        </el-tag>
    </div>
</template>

<script>
  import {mapGetters, mapMutations} from 'vuex'

  export default {
    name: "CommonTab",
    computed: {
      ...mapGetters([
        "getTabs"
      ])
    },
    methods: {
      ...mapMutations({
        close: "closeTab"
      }),
      handleClose(tag) {
        // 如果关闭的是当前页面，需要跳转路由到上一个 (主页)
        if (this.$route.name === tag.name) {
          this.close(tag);
          this.$router.push({name: "home"})
        } else {
          this.close(tag)
        }
      },
      changeMenu(item) {
        if (item.name !== this.$route.name) {
          this.$router.push({name: item.name});
          this.$store.dispatch("setItem", item)
        }
      }
    }
  }
</script>

<style scoped>
    .tab {
        margin: 5px 0 0 10px;
        cursor: default;
    }

    .el-tag {
        margin-right: 10px;
    }
</style>