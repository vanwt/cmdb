<template>
<!--     组件路径是 url   URL 是path-->
    <div class="usertab">
        <el-dialog :title="operateType === 'add' ? '添加菜单' : '修改菜单'" :visible.sync="visible"
                   close-on-press-escape center fullscreen>
            <el-form ref="menuForm" :model="menu">
                <el-divider content-position="center">基础信息</el-divider>
                <el-row type="fiex" justify="space-between">
                    <el-col :span="6">
                        <el-form-item label="菜单名" prop="title">
                            <el-input v-model="menu.title"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="组件路径" prop="url">
                            <el-input v-model="menu.url"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="URL" prop="url">
                            <el-input v-model="menu.path"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="组件别名" prop="name">
                            <el-input v-model="menu.name"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row type="fiex">
                    <el-col :span="6">
                        <el-form-item label="状态" prop="status">
                            <el-switch style="margin-right: 15px;"
                                       v-model="menu.status"
                                       active-text="启用"
                                       inactive-text="禁用">
                            </el-switch>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item prop="is_parent">
                            <el-checkbox v-model="menu.is_parent">是否为父组件</el-checkbox>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="父组件" prop="parent" v-if="!menu.is_parent">
                            <el-select v-model="menu.parent" placeholder="请选择父组件">
                                <el-option :label="item.label" :value="item.value" :key="k"
                                           v-for="(item,k) in menus"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="图标" prop="icon">
                            <el-input v-model="menu.icon"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer">
                <el-button type="primary" @click="menuSubmit('userForm')">提交</el-button>
                <el-button @click="visible=false">取消</el-button>
            </span>
        </el-dialog>
        <div class="mytab-header">
            <el-form :inline="true" :model="config">
                <el-form-item>
                    <el-button type="primary" @click="addMenu">添加</el-button>
                    <el-button type="danger" @click="deleteMenu">删除</el-button>
                    <el-tooltip effect="dark" content="刷新列表" placement="top">
                        <el-button type="warning" plain @click="getMenuTableData"
                                   icon="el-icon-refresh"></el-button>
                    </el-tooltip>
                </el-form-item>
            </el-form>
        </div>
        <el-table class="commonTable"
                  ref="menuTable"
                  tooltip-effect="dark"
                  style="width: 100%"
                  height="100%"
                  @selection-change="handleSelectionChange"
                  :data="tableData"
                  row-key="key"
                  border
                  default-expand-all
                  :tree-props="{children: 'children'}">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column
                    prop="title"
                    label="菜单名"
                    sortable>
            </el-table-column>
            <el-table-column prop="path" label="URL"></el-table-column>
            <el-table-column prop="url" label="组件路径"></el-table-column>
            <el-table-column prop="name" label="别名" sortable></el-table-column>
            <el-table-column prop="icon" label="图标"></el-table-column>
            <el-table-column prop="status" label="状态">
                <template slot-scope="scope">
                    <el-tag type="success" v-show="scope.row.status">启用</el-tag>
                    <el-tag type="danger" v-show="!scope.row.status">关闭</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button type="warning" plain size="mini" @click="editMenu(scope.row)">Edit</el-button>
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
        menu: {
          title: "",
          status: true,
          url: "",
          path: "",
          name: "",
          is_parent: false,
          parent: "",
          icon: ""
        },
        // 数据
        // 表单数据
        tableData: [],
        menus: [],
        //======================================================
        // 左侧选择数据
        Selection: [],
        // 页面配置
        config:
          {
            page: 1,
            page_size:
              10,
            total:
            undefined,
            select:
              'title',
            search:
              "",
          }
      }
    },
    methods: {
      getMenuTableData(event, my_url) {
        if (!my_url) {
          my_url = `api/v1/menu?page=${this.config.page}&limit=${this.config.page_size}`;
        }
        this.$http.get(my_url)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.tableData = resp.data.data;
            this.config.total = resp.data.count;
            resp.data.data.forEach(item => {
              this.menus.push({
                label: item.title,
                value: item.id
              })
            })
          }).catch(err => {
          console.log(err)
        });
      },
      addMenu() {
        this.menu = {
          title: "",
          status: true,
          url: "",
          path: "",
          name: "",
          is_parent: false,
          parent: "",
          icon: ""
        };
        this.operateType = "add";
        this.visible = true
      },
      editMenu(row) {
        this.$http.get(`api/v1/menu/${row.id}/`)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.menu = resp.data;
            this.operateType = 'edit';
            this.visible = true
          }).catch(err => {
          this.$alert('未找到该用户,可能由于后台已删除,请刷新！', '错误', {
            confirmButtonText: '确定',
          });
          console.log(err)
        })
      },
      deleteMenu() {
        let id_list = [];
        this.Selection.forEach(obj => {
          id_list.push(obj.id)
        });
        // 发送delete 请求
        let param = {ids: id_list};
        this.$http.delete("api/v1/menu/", {data: param})
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.$message({
              message: '删除成功！',
              type: 'success'
            });
            // 刷新表格
            this.getMenuTableData()
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了',
            duration: 0
          });
          console.log(err)
        })
      },

      menuSubmit() {
        this.$confirm('确定要提交吗, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            if (this.operateType === 'add') {
              // 执行添加
              this.$http.post('api/v1/menu/', this.menu).then(resp => {
                // 需要将 tag id 转换 text/value tag name 转化 value/label
                this.$message({
                  message: '恭喜，添加成功！',
                  type: 'success'
                });
                this.visible = false;
                // 刷新表格
                this.getMenuTableData()
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
              this.$http.put(`api/v1/menu/${this.menu.id}/`, this.menu, {
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
                this.getMenuTableData()
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
        this.getMenuTableData()
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.config.page = val;
        this.getMenuTableData()
      }
    },
    created() {
      this.getMenuTableData();
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