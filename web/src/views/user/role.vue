<template>
    <div class="usertab">
        <el-dialog :title="operateType === 'add' ? '添加角色' : '修改角色'" :visible.sync="visible"
                   close-on-press-escape center fullscreen>
            <el-form ref="assetsForm" :model="role">
                <el-divider content-position="center">基础信息</el-divider>
                <el-row type="fiex" justify="space-between">
                    <el-col :span="6" :offset="9">
                        <el-form-item label="角色名" prop="title">
                            <el-input v-model="role.title"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="6" :offset="9">
                        <el-form-item label="状态" prop="status">
                            <el-switch style="margin-right: 15px;"
                                       v-model="role.status"
                                       active-text="启用"
                                       inactive-text="禁用">
                            </el-switch>
                        </el-form-item>
                    </el-col>
                </el-row>

            </el-form>
            <span slot="footer">
                <el-button type="primary" @click="roleSubmit">提交</el-button>
                <el-button @click="visible=false">取消</el-button>
            </span>
        </el-dialog>
        <common-transfer :value="transfer_value" :data="transfer_data" :title="transfer_title"
                         :visible.sync="transfer" @Close="transfer=false" @Submit="transferSubmit"></common-transfer>
        <div class="mytab-header">
            <el-form :inline="true" :model="config">
                <el-form-item>
                    <el-button type="primary" @click="addRole">添加</el-button>
                    <el-button type="danger" @click="deleteRole">删除</el-button>
                    <el-tooltip effect="dark" content="刷新列表" placement="top">
                        <el-button type="warning" plain @click="getRoleTableData"
                                   icon="el-icon-refresh"></el-button>
                    </el-tooltip>
                </el-form-item>
            </el-form>
        </div>
        <el-table border class="commonTable"
                  ref="roleTable"
                  :data="tableData"
                  tooltip-effect="dark"
                  style="width: 100%"
                  height="100%"
                  @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="title" label="角色名"></el-table-column>
            <el-table-column prop="status" label="状态">
                <template slot-scope="scope">
                    <el-tag type="success" v-show="scope.row.status">启用</el-tag>
                    <el-tag type="danger" v-show="!scope.row.status">关闭</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button type="default" plain size="mini" @click="editRole(scope.row)">Edit</el-button>
                    <el-button type="success" size="mini" plain @click="editMenu(scope.row)">菜单</el-button>
                    <el-button type="warning" size="mini" plain @click="editPermission(scope.row)">权限</el-button>
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
  import CommonTransfer from "@/components/CommonTransfer";

  export default {
    data() {
      return {
        // 添加操作,或者 edit 修改
        operateType: 'add',
        // 是否显示dialog
        visible: false,
        role: {
          title: "",
          status: true
        },
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
            total: undefined,
            select: 'title',
            search: "",
          },
        // transf
        transfer: false,
        transfer_title: "Permission",
        transfer_value: [],
        transfer_data: [],
        checked: []
      }
    },
    methods: {
      getRoleTableData(event, my_url) {
        if (!my_url) {
          my_url = `api/v1/role?page=${this.config.page}&limit=${this.config.page_size}`;
        }
        this.$http.get(my_url)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            console.log(resp.data);
            this.tableData = resp.data.data;
            this.config.total = resp.data.count;
          }).catch(err => {
          console.log(err)
        })
      },
      addRole() {
        this.role = {
          title: "",
          status: true
        };
        this.operateType = "add";
        this.visible = true
      },
      editRole(row) {
        this.$http.get(`api/v1/role/${row.id}/`)
          .then(resp => {
            this.role = {};
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.role = resp.data;
            this.operateType = 'edit';
            this.visible = true
          }).catch(err => {
          this.$alert('未找到该用户,可能由于后台已删除,请刷新！', '错误', {
            confirmButtonText: '确定',
          });
          console.log(err)
        })
      },
      deleteRole() {
        let id_list = [];
        this.Selection.forEach(obj => {
          id_list.push(obj.id)
        });
        // 发送delete 请求
        let param = {ids: id_list};
        this.$http.delete("api/v1/role/", {data: param})
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.$message({
              message: '删除成功！',
              type: 'success'
            });
            // 刷新表格
            this.getRoleTableData()
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了',
            duration: 0
          });
          console.log(err)
        })
      },
      roleSubmit() {
        this.$confirm('确定要提交吗, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            if (this.operateType === 'add') {
              // 执行添加
              this.$http.post('api/v1/role/', this.role).then(resp => {
                console.log(resp)
                // 需要将 tag id 转换 text/value tag name 转化 value/label
                this.$message({
                  message: '恭喜，添加成功！',
                  type: 'success'
                });
                this.visible = false;
                // 刷新表格
                this.getRoleTableData()
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
              console.log(this.role)
              this.$http.put(`api/v1/role/${this.role.id}/`, this.role).then(resp => {
                // 需要将 tag id 转换 text/value tag name 转化 value/label
                console.log(resp.data);
                this.$message({
                  message: '恭喜，修改成功！',
                  type: 'success'
                });
                this.visible = false;
                // 刷新表格
                this.getRoleTableData()
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

      editPermission(row) {
        this.transfer_value = [];
        this.transfer_data = [];
        this.$http.get(`api/v1/role/permission/${row.id}/`)
          .then(resp => {
            this.role = {};
            this.transfer_title = "Permission";
            this.transfer = true;
            this.role = row;
            resp.data.permissions.forEach(item => {
              this.transfer_data.push({
                label: item.title,
                key: item.value
              })
            });
            this.transfer_value = resp.data.checked
          }).catch(err => {
          this.$alert('未找到该角色,可能由于后台已删除,请刷新！', '错误', {
            confirmButtonText: '确定',
          });
          console.log(err)
        });
        //得到 所有权限 和已选权限
      },
      editMenu(row) {
        this.transfer_value = [];
        this.transfer_data = [];

        this.$http.get(`api/v1/role/menu/${row.id}/`)
          .then(resp => {
            this.transfer_title = "Menu";
            this.transfer = true;
            this.role = row;
            resp.data.menus.forEach(item => {
              this.transfer_data.push({
                label: item.title,
                key: item.value
              })
            });
            this.transfer_value = resp.data.checked
          }).catch(err => {
          this.$alert('未找到该角色,可能由于后台已删除,请刷新！', '错误', {
            confirmButtonText: '确定',
          });
          console.log(err)
        });
      },
      transferSubmit(val) {
        if (this.transfer_title === "Permission") {
          this.$http.post(`api/v1/role/permission/${this.role.id}/`, {ids: val})
            .then(resp => {
              this.$message({
                message: '修改成功！',
                type: 'success'
              });
            }).catch(err => {
            this.$alert('失败！' + err.message, '错误', {
              confirmButtonText: '确定',
            });
            console.log(err)
          });
        } else {
          this.$http.post(`api/v1/role/menu/${this.role.id}/`, {ids: val})
            .then(resp => {
              this.$message({
                message: '修改成功！',
                type: 'success'
              });
              this.transfer = false
            }).catch(err => {
            this.$alert('失败！' + err.message, '错误', {
              confirmButtonText: '确定',
            });
            console.log(err)
          });
        }
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
        this.getRoleTableData()
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.config.page = val;
        this.getRoleTableData()
      },
    },
    components: {
      CommonTransfer
    },
    created() {
      this.getRoleTableData();
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