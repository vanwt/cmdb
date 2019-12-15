<template>
    <div class="usertab">
        <el-dialog :title="operateType === 'add' ? '添加用户' : '修改用户'" :visible.sync="visible"
                   close-on-press-escape center fullscreen>
            <el-form ref="assetsForm" :model="user">
                <el-divider content-position="center">基础信息</el-divider>
                <el-row type="fiex" justify="space-between">
                    <el-col :span="6" :offset="3">
                        <el-form-item label="用户名" prop="username">
                            <el-input v-model="user.username"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="真实姓名" prop="realname">
                            <el-input v-model="user.realname"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6" v-if="operateType==='add'">
                        <el-form-item label="用户密码" prop="password">
                            <el-input v-model="user.password"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-divider content-position="center">其他信息</el-divider>
                <el-row type="fiex">
                    <el-col :span="6" :offset="3">
                        <el-form-item label="手机号" prop="phone">
                            <el-input v-model="user.phone"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="user.email"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="备注" prop="remark">
                            <el-input v-model="user.remark"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer">
                <el-switch style="margin-right: 15px;" v-if="operateType==='add'"
                           v-model="user.many"
                           active-text="多"
                           inactive-text="单">
                </el-switch>
                <el-button type="primary" @click="userSubmit('userForm')">提交</el-button>
                <el-button @click="visible=false">取消</el-button>
            </span>
        </el-dialog>
        <el-dialog title="角色变更" :visible.sync="role_visible"
                   close-on-press-escape center>
            <el-transfer
                    filterable
                    filter-placeholder="输入"
                    v-model="role_value"
                    :data="role_data"
                    :titles="['全部角色', '已选角色']"
                    :right-default-checked="right_checked"
            >
            </el-transfer>
            <span slot="footer">
                <el-button type="primary" @click="changeRoleSubmit">提交</el-button>
                <el-button @click="role_visible=false">取消</el-button>
            </span>
        </el-dialog>
        <div class="mytab-header">
            <el-form :inline="true" :model="config">
                <el-form-item>
                    <el-input placeholder="请输入内容" clearable v-model="config.search">
                        <el-select style="width: 130px;" v-model="config.select" slot="prepend" placeholder="请选择">
                            <el-option value="realname" label="姓名匹配"></el-option>
                            <el-option value="username" label="用户名匹配"></el-option>
                        </el-select>
                    </el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" icon="el-icon-search" @click="searchUser">搜索</el-button>
                    <el-button type="primary" @click="addUser">添加</el-button>
                    <el-button type="danger" @click="deleteUser">删除</el-button>
                    <el-tooltip effect="dark" content="刷新列表" placement="top">
                        <el-button type="warning" plain @click="getUserTableData"
                                   icon="el-icon-refresh"></el-button>
                    </el-tooltip>
                    <el-tooltip effect="dark" content="导出到Excel" placement="top">
                        <el-button icon="el-icon-download" @click="exportExcel"></el-button>
                    </el-tooltip>
                </el-form-item>
            </el-form>
        </div>
        <el-table border class="commonTable"
                  ref="userTable"
                  :data="tableData"
                  tooltip-effect="dark"
                  style="width: 100%"
                  height="100%"
                  @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="realname" label="真实姓名"></el-table-column>
            <el-table-column prop="phone" label="电话"></el-table-column>
            <el-table-column prop="roles" label="角色">
                <template slot-scope="scope">
                    <el-tag v-for="item in scope.row.roles" :key="item[1]" type="success" size="mini">
                        {{ item[1] }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="last_login" label="上次登录"></el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button type="warning" plain size="mini" @click="editUser(scope.row)">Edit</el-button>
                    <el-button type="primary" size="mini" plain @click="changUserRole(scope.row)">角色变更</el-button>
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
        user: {
          username: "",
          realname: "",
          password: "",
          email: "",
          phone: "",
          remark: "",
          many: false
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
            page_size:
              10,
            total:
            undefined,
            select:
              'realname',
            search:
              "",
          },
        // role
        role_value: [],
        role_data: [],
        role_visible: false,
        all_roles: [],
        right_checked: [],
        user_id: undefined
      }
    },
    methods: {
      getUserTableData(event, my_url) {
        if (!my_url) {
          my_url = `api/v1/user?page=${this.config.page}&limit=${this.config.page_size}`;
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
      addUser() {
        this.user = {
          username: "",
          realname: "",
          password: "",
          email: "",
          phone: "",
          remark: "",
          many: false
        };
        this.operateType = "add";
        this.visible = true
      },
      editUser(row) {
        this.$http.get(`api/v1/user/${row.id}/`)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.user = resp.data;
            this.operateType = 'edit';
            this.visible = true
          }).catch(err => {
          this.$alert('未找到该用户,可能由于后台已删除,请刷新！', '错误', {
            confirmButtonText: '确定',
          });
          console.log(err)
        })
      },
      searchUser() {
        let url = `api/v1/user/?${this.config.select}=${this.config.search}`;
        this.getUserTableData(undefined, url)
      },
      deleteUser() {
        let id_list = [];
        this.Selection.forEach(obj => {
          id_list.push(obj.id)
        });
        // 发送delete 请求
        let param = {ids: id_list};
        this.$http.delete("api/v1/user/", {data: param})
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.$message({
              message: '删除成功！',
              type: 'success'
            });
            // 刷新表格
            this.getUserTableData()
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了',
            duration: 0
          });
          console.log(err)
        })
      },
      changUserRole(row) {
        this.user_id = undefined;
        // 请求 用户de role
        this.$http.get(`api/v1/user/role/${row.id}/`)
          .then(resp => {
            // 需要将 role 的title/value 转换 label/key   value/key 时角色id
            resp.data.roles.forEach(role => {
              this.role_data.push({
                label: role.title,
                key: role.value
              })
            });
            // 得到已选的
            this.right_checked = resp.data.selected;
            this.role_visible = true
          })
          .catch(err => {
            this.$alert('未找到该用户,可能由于后台已删除,请刷新！', '错误', {
              confirmButtonText: '确定',
            });
          });
        this.role_value = [];
        this.user_id = row.id;
        this.role_visible = true
      },
      changeRoleSubmit() {
        console.log(this.role_value);
        this.$http.put(`api/v1/user/role/${this.user_id}/`, {"selected": this.role_value})
          .then(resp => {
            // 需要将 role 的title/value 转换 label/key   value/key 时角色id
            this.$message({
              message: '恭喜，修改角色成功！',
              type: 'success'
            });
            this.role_visible = false;
            this.getUserTableData()
          })
          .catch(err => {
            this.$alert('未找到该用户,可能由于后台已删除,请刷新！', '错误', {
              confirmButtonText: '确定',
            });
          });
      },
      userSubmit() {
        this.$confirm('确定要提交吗, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            if (this.operateType === 'add') {
              // 执行添加
              this.$http.post('api/v1/user/', this.user, {
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
                this.getUserTableData()
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
              console.log(this.user.id)
              this.$http.put(`api/v1/user/${this.user.id}/`, this.user, {
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
                this.getUserTableData()
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
        this.getUserTableData()
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.config.page = val;
        this.getUserTableData()
      },
      exportExcel() {
        let wb = XLSX.utils.table_to_book(document.querySelector('.el-table__body'), {raw: true});
        let wbout = XLSX.write(wb, {bookType: 'xlsx', bookSST: true, type: 'array'});
        try {
          FileSaver.saveAs(new Blob([wbout], {type: 'application/octet-stream'}), '用户.xlsx')
        } catch (e) {
          if (typeof console !== 'undefined') console.log(e, wbout)
        }
        return wbout
      }
    }
    ,
    created() {
      this.getUserTableData();
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