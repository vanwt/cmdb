<template>
    <div class="commonTable">
        <el-table :data="tableData" height="95%" stripe>
            <el-table-column label="序号"
                    type="selection"
                    width="55">
            </el-table-column>
            <!--            prop是对应列的字段名-->
            <el-table-column show-overflow-tooltip v-for="item in tableLabel" :key="item.prop" :prop="item.prop"
                             :label="item.label">
                <!--                scope 相当于这个列的数据-->
                <template slot-scope="scope">
                    <span style="margin-left: 10px">{{ scope.row[item.prop] }}</span>
                </template>
            </el-table-column>

            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button
                            size="mini"
                            @click="handleEdit(scope.row)">编辑
                    </el-button>
                    <el-button
                            size="mini"
                            type="danger"
                            @click="handleDelete(scope.row)">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination class="pager"
                layout="prev, pager, next" background
                :total="config.total" :curre-page.sync="config.page"
                       @current-change="changePage">
        </el-pagination>
    </div>
</template>

<script>
  export default {
    name: "CommonTable",
    props: {
      tableLabel: Array,
      tableData: Array,
      config: Object
    },
    methods:{
      handleEdit(row){
        this.$emit('Edit',row)
      },
      handleDelete(row){
        this.$emit('Delete',row)
      },
      changePage(page){
        this.$emit('changePage',page)
      }
    },
  }
</script>

<style scoped lang="scss">
    .commonTable {
        height: calc(100% - 62px);
        position: relative;
        .pager {
            border: 0;
            position: absolute;
            right: 100px;
        }
    }
</style>