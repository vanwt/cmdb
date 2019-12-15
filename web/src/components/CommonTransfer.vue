<template>
    <el-dialog :title="title" :visible.sync="visible"
               close-on-press-escape center :before-close="closeDialog">
        <el-transfer style="width: 100%"
                filterable
                filter-placeholder="输入"
                v-model="value"
                :data="data"
                :titles="['未选','已选']"
                :right-default-checked="checked">
        </el-transfer>
        <span slot="footer">
                <el-button type="primary" @click="transferSubmit">提交</el-button>
                <el-button @click="closeDialog">取消</el-button>
            </span>
    </el-dialog>
</template>

<script>
  export default {
    name: "CommonTransfer",
    props: {
      title: String,
      visible: Boolean,
      data: Array,
      value: Array,
      checked: Array
    },
    methods: {
      transferSubmit() {
        this.$emit("Submit", this.value)
      },
      closeDialog() {
        this.$emit("Close")
      }
    }
  }
</script>

<style scoped>
    .el-transfer-panel{
        width: 280px;
    }
</style>