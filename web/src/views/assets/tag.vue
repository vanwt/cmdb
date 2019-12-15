<template>
    <div class="tagtab">
        <el-dialog :title="operateType === 'add' ? '添加标签' : '修改标签'" :visible.sync="visible"
                   close-on-press-escape center fullscreen>
            <el-form ref="assetsForm" :model="tag">
                <el-divider content-position="center">基础信息</el-divider>
                <el-row type="fiex" justify="space-between">
                    <el-col :span="6" :offset="8">
                        <el-form-item label="标签名" prop="name">
                            <el-input v-model="tag.name"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer">
                <el-button type="primary" @click="tagSubmit('tagForm')">提交</el-button>
                <el-button @click="visible=false">取消</el-button>
            </span>
        </el-dialog>
        <div class="mytab-header">
            <el-form :inline="true" :model="config">
                <el-form-item>
                    <el-button type="primary" @click="addTag">添加</el-button>
                    <el-button type="danger" @click="deleteTag">删除</el-button>
                    <el-tooltip effect="dark" content="刷新列表" placement="top">
                        <el-button type="warning" plain @click="getTagTableData"
                                   icon="el-icon-refresh"></el-button>
                    </el-tooltip>
                </el-form-item>
            </el-form>
        </div>
        <el-table border class="commonTable"
                  ref="tagTable"
                  :data="tableData"
                  tooltip-effect="dark"
                  style="width: 100%"
                  @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="name" label="标签名"></el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button type="warning" plain size="mini" @click="editTag(scope.row)">Edit</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination class="pager"
                       @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"
                       :current-page="config.page"
                       :page-sizes="[10, 15,20]"
                       :page-size="config.page_size"
                       layout="total, sizes, prev, pager, next, jumper"
                       background
                       :total="config.total">
        </el-pagination>
    </div>
</template>

<script>

  export default {
    data() {
      return {
        // 添加操作,或者 edit 修改
        operateType: 'add',
        // 是否显示dialog
        visible: false,
        tag: {
          name: "",
        },

        // 数据
        // 表单数据
        tableData: [],
        // 左侧选择数据
        Selection:
          [],
        // 页面配置
        config:
          {
            page: 1,
            page_size: 10,
            total: undefined
          },
      }
    },
    methods: {
      getTagTableData(event, my_url) {
        if (!my_url) {
          my_url = `/api/v1/tag?page=${this.config.page}&limit=${this.config.page_size}`
        }
        this.$http.get(my_url)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.tableData = resp.data.data;
            this.config.total = resp.data.count;
          }).catch(err => {
          this.$message.error('标签加载失败!');
        })
      },
      addTag() {
        this.tag = {
          name: "",
        };
        this.operateType = "add";
        this.visible = true
      },
      editTag(row) {
        this.$http.get(`api/v1/tag/${row.id}/`)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.tag = resp.data;
            this.operateType = 'edit';
            this.visible = true
          }).catch(err => {
          this.$alert('未找到该用户,可能由于后台已删除,请刷新！', '错误', {
            confirmButtonText: '确定',
          });
          console.log(err)
        })
      },
      deleteTag() {
        let id_list = [];
        this.Selection.forEach(obj => {
          id_list.push(obj.id)
        });
        // 发送delete 请求
        let param = {ids: id_list};
        this.$http.delete("api/v1/tag/", {data: param})
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.$message({
              message: '删除成功！',
              type: 'success'
            });
            // 刷新表格
            this.getTagTableData()
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了',
            duration: 0
          });
          console.log(err)
        })
      },
      tagSubmit() {
        this.$confirm('确定要提交吗, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            if (this.operateType === 'add') {
              // 执行添加
              this.$http.post('api/v1/tag/', this.tag, {
                transformRequest: [function (data) {
                  let params = "";
                  for (let index in data) {
                    params += index + "=" + data[index] + "&"
                  }
                  return params
                }]
              }).then(resp => {
                // 需要将 tag id 转换 text/value tag name 转化 value/label
                this.$message({
                  message: '恭喜，添加成功！',
                  type: 'success'
                });
                this.visible = false;
                // 刷新表格
                this.getTagTableData()
              }).catch(err => {
                this.$notify.error({
                  title: '错误',
                  message: '出错了:' + err.data.message,
                  duration: 0
                });
                console.log(err)
              })
            } else {
              // 执行修改
              this.$http.put(`api/v1/tag/${this.tag.id}/`, this.tag, {
                transformRequest: [function (data) {
                  let params = "";
                  for (let index in data) {
                    params += index + "=" + data[index] + "&"
                  }
                  return params
                }]
              }).then(resp => {
                // 需要将 tag id 转换 text/value tag name 转化 value/label
                this.$message({
                  message: '恭喜，修改成功！',
                  type: 'success'
                });
                this.visible = false;
                // 刷新表格
                this.getTagTableData()
              }).catch(err => {
                this.$notify.error({
                  title: '错误',
                  message: '出错了:' + err.data.message,
                  duration: 0
                });
                console.log(err)
              })
            }
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消提交'
            });
          });
      },
      // 多选 点击后获得选中数据
      handleSelectionChange(val) {
        this.Selection = val;
      },
      handleSizeChange(val) {
        // console.log(`每页 ${val} 条`);
        this.config.page_size = val;
        this.getTagTableData()
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.config.page = val;
        this.getTagTableData()
      }
    },
    created() {
      this.getTagTableData();
    }
  }
</script>

<style scoped lang="scss">
    .tagtab {
        height: 85%;
        padding-bottom: 15px;
        /*overflow: hidden;*/

        .el-button {
            margin-right: 5px;
        }

        &-header {
            display: inline-flex;
            justify-content: space-between;
            align-items: flex-start;

            .el-select {
                width: 130px;
            }
        }

        .commonTable {
            height: calc(100% - 65px);
            position: relative;

        }

        .pager {
            border: 0;
            position: absolute;
            right: 100px;
            margin-top: 20px;
        }
    }
</style>