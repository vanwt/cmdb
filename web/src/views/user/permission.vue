<template>
    <div class="usertab">
        <el-dialog :title="operateType === 'add' ? '添加权限' : '修改权限'" :visible.sync="visible"
                   close-on-press-escape center fullscreen>
            <el-form ref="purviewForm" :model="purview">
                <el-divider content-position="center">基础信息</el-divider>
                <el-row type="fiex" justify="space-between">
                    <el-col :span="6" :offset="6">
                        <el-form-item label="权限名" prop="title">
                            <el-input v-model="purview.title"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6" :offset="1">
                        <el-form-item label="URL" prop="url">
                            <el-input v-model="purview.url"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row type="fiex">
                    <el-col :span="6" :offset="6">
                        <el-form-item label="请求类型" prop="method">
                            <el-select v-model="purview.method" placeholder="请选择请求类型">
                                <el-option label="GET" value="GET"></el-option>
                                <el-option label="POST" value="POST"></el-option>
                                <el-option label="PUT" value="PUT"></el-option>
                                <el-option label="DELETE" value="DELETE"></el-option>
                                <el-option label="ALL" value="ALL"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6" :offset="1">
                        <el-form-item label="状态" prop="status">
                            <el-switch style="margin-right: 15px;"
                                       v-model="purview.status"
                                       active-text="启用"
                                       inactive-text="禁用">
                            </el-switch>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer">
                <el-button type="primary" @click="purviewSubmit('userForm')">提交</el-button>
                <el-button @click="visible=false">取消</el-button>
            </span>
        </el-dialog>
        <div class="mytab-header">
            <el-form :inline="true" :model="config">
                <el-form-item>
                    <el-button type="primary" @click="addPurview">添加</el-button>
                    <el-button type="danger" @click="deletePurview">删除</el-button>
                    <el-tooltip effect="dark" content="刷新列表" placement="top">
                        <el-button type="warning" plain @click="getPurviewTableData"
                                   icon="el-icon-refresh"></el-button>
                    </el-tooltip>
                </el-form-item>
            </el-form>
        </div>
        <el-table border class="commonTable"
                  ref="purviewTable"
                  :data="tableData"
                  tooltip-effect="dark"
                  style="width: 100%"
                  height="100%"
                  @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="title" label="权限名"></el-table-column>
            <el-table-column prop="url" label="URL"></el-table-column>
            <el-table-column prop="method" label="请求类型"></el-table-column>
            <el-table-column prop="status" label="状态">
                <template slot-scope="scope">
                    <el-tag type="success" v-show="scope.row.status">启用</el-tag>
                    <el-tag type="danger" v-show="!scope.row.status">关闭</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button type="warning" plain size="mini" @click="editPurview(scope.row)">Edit</el-button>
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
  import FileSaver from 'file-saver';
  import XLSX from 'xlsx'

  export default {
    data() {
      return {
        // 添加操作,或者 edit 修改
        operateType: 'add',
        // 是否显示dialog
        visible: false,
        purview: {
          title: "",
          status: true,
          method: "GET",
          url: "",
        },
        // 数据
        // 表单数据
        tableData: [],
        // 左侧选择数据
        Selection: [],
        // 页面配置
        config: {
          page: 1,
          page_size: 10,
          total: undefined,
          select: 'title',
          search: "",
        }
      }
    },
    methods: {
      getPurviewTableData(event, my_url) {
        if (!my_url) {
          my_url = `api/v1/permission?page=${this.config.page}&limit=${this.config.page_size}`;
        }
        this.$http.get(my_url)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.tableData = resp.data.data;
            this.config.total = resp.data.count;
          }).catch(err => {
          console.log(err)
        })
      },
      addPurview() {
        this.purview = {
          title: "",
          status: true,
          method: "GET",
          url: "",
        };
        this.operateType = "add";
        this.visible = true
      },
      editPurview(row) {
        this.$http.get(`api/v1/permission/${row.id}/`)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.purview = resp.data;
            this.operateType = 'edit';
            this.visible = true
          }).catch(err => {
          this.$alert('未找到该用户,可能由于后台已删除,请刷新！', '错误', {
            confirmButtonText: '确定',
          });
          console.log(err)
        })
      },
      deletePurview() {
        let id_list = [];
        this.Selection.forEach(obj => {
          id_list.push(obj.id)
        });
        // 发送delete 请求
        let param = {ids: id_list};
        this.$http.delete("api/v1/permission/", {data: param})
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.$message({
              message: '删除成功！',
              type: 'success'
            });
            // 刷新表格
            this.getPurviewTableData()
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了',
            duration: 0
          });
          console.log(err)
        })
      },

      purviewSubmit() {
        this.$confirm('确定要提交吗, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            if (this.operateType === 'add') {
              // 执行添加
              this.$http.post('api/v1/permission/', this.purview).then(resp => {
                // 需要将 tag id 转换 text/value tag name 转化 value/label
                this.$message({
                  message: '恭喜，添加成功！',
                  type: 'success'
                });
                this.visible = false;
                // 刷新表格
                this.getPurviewTableData()
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
              this.$http.put(`api/v1/permission/${this.purview.id}/`, this.purview, {
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
                this.getPurviewTableData()
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
      clearFilter() {
        this.$refs.userTable.clearFilter();
      },
      // 多选 点击后获得选中数据
      handleSelectionChange(val) {
        this.Selection = val;
      },
      handleSizeChange(val) {
        // console.log(`每页 ${val} 条`);
        this.config.page_size = val;
        this.getPurviewTableData()
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.config.page = val;
        this.getPurviewTableData()
      }
    },
    created() {
      this.getPurviewTableData();
    }
  }
</script>

<style scoped lang="scss">
    .usertab {
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