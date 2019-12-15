<template>
    <div class="mytab">
        <assets-form :assets="assets" :visible="visible" @assetsSubmit="assetsSubmit" @dialogClose="visible=false"
                     :operateType="operateType" :tag_list="tag_list" :idc_list="idc_list"
                     :user_list="user_list" :host_machine_list="host_machine_list"></assets-form>
        <div class="mytab-header">
            <el-form :inline="true" :model="config">
                <el-form-item>
                    <el-input placeholder="请输入内容" clearable v-model="config.search">
                        <el-select v-model="config.select" slot="prepend" placeholder="请选择">
                            <el-option value="ip" label="IP"></el-option>
                            <el-option value="sshuser" label="登录账户"></el-option>
                            <el-option value="mysql_user" label="MYSQL用户"></el-option>
                            <el-option value="mysql_port" label="MYSQL端口"></el-option>
                        </el-select>
                    </el-input>
                </el-form-item>

                <el-popover
                        placement="bottom"
                        title="标题"
                        width="200"
                        trigger="click">
                    <el-form-item>
                        <el-checkbox v-model="config.showCreateTime">创建时间</el-checkbox>
                        <el-checkbox v-model="config.showKefu">客服</el-checkbox>
                        <el-checkbox v-model="config.showOps">运维</el-checkbox>
                    </el-form-item>
                    <el-button slot="reference">隐藏列</el-button>
                </el-popover>


                <el-form-item>
                    <el-button type="primary" icon="el-icon-search" @click="searchAssets">搜索</el-button>
                    <el-button type="primary" @click="assetsAdd">添加</el-button>
                    <el-button type="danger" @click="deleteAssets">删除</el-button>
                    <el-tooltip effect="dark" content="重置筛选" placement="top">
                        <el-button @click="clearFilter" icon="el-icon-refresh"></el-button>
                    </el-tooltip>
                    <el-tooltip effect="dark" content="刷新列表" placement="top">
                        <el-button type="warning" plain @click="getAssetsTableData" icon="el-icon-refresh"></el-button>
                    </el-tooltip>
                    <el-tooltip effect="dark" content="导出到Excel" placement="top">
                        <el-button icon="el-icon-download" @click="exportExcel"></el-button>
                    </el-tooltip>
                </el-form-item>
            </el-form>
        </div>
        <el-table border class="commonTable"
                  ref="assetsTable"
                  :data="tableData"
                  tooltip-effect="dark"
                  style="width: 100%"
                  height="100%"
                  @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55"></el-table-column>
            <el-table-column prop="ip" label="IP" width="140"></el-table-column>
            <el-table-column prop="asset_type" label="资产类型" width="80"></el-table-column>
            <el-table-column prop="system" label="系统" width="100"></el-table-column>
            <el-table-column prop="idc" label="机房" width="100" :filters="filter_idc_list"
                             :filter-method="filterIdc"></el-table-column>
            <el-table-column prop="tags" label="标签"
                             :filters="filter_tag_list"
                             :filter-method="filterTag">
                <template slot-scope="scope">
                    <el-tag style="margin-right: 3px;" size="mini" v-for="tag in scope.row.tags" :key="tag"
                            effect="dark" type="info">
                        {{tag}}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80" :filters="filter_status_list"
                             :filter-method="filterStatus">
                <template slot-scope="scope">
                    <el-tag
                            :type="scope.row.status === '启用' ? 'success' :  scope.row.status === '下架' ? 'danger' : scope.row.status === '故障' ? 'warning' : 'info'"
                            effect="plain">
                        {{ scope.row.status }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="host_machine" label="宿主机"></el-table-column>
            <el-table-column prop="kefu" label="客服" width='80' v-if="config.showKefu"></el-table-column>
            <el-table-column prop="opsuser" label="运维" width='80' v-if="config.showOps"></el-table-column>
            <el-table-column prop="create_time" label="创建时间" v-if="config.showCreateTime"></el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button type="primary" size="mini" plain @click="assetsInfo(scope.row)">Info</el-button>
                    <el-button type="warning" plain size="mini" @click="assetsEdit(scope.row)">Edit</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination class="pager"
                       @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"
                       :current-page="config.page"
                       :page-sizes="[10, 30, 60, 100,200]"
                       :page-size="config.page_size"
                       layout="total, sizes, prev, pager, next, jumper"
                       background
                       :total="config.total">
        </el-pagination>
    </div>
</template>

<script>
  import AssetsForm from "@/components/AssetsForm";
  import FileSaver from 'file-saver';
  import XLSX from 'xlsx'

  export default {
    components: {
      AssetsForm
    },
    data() {
      return {
        // 添加操作,或者 edit 修改
        operateType: 'add',
        // 是否显示dialog
        visible: false,
        // 数据
        // 表单数据
        assets: {},
        default_assets: {
          asset_type: '1',
          ftp_port: '',
          host_machine: '',
          idc: '',
          ip: '',
          kefu: '',
          mysql_port: '',
          mysql_pwd: '',
          mysql_user: '',
          ops_user: '',
          remark: '',
          sshport: '',
          sshpwd: '',
          sshkey: '',
          sshyubico: '',
          sshuser: '',
          status: '1',
          system: '',
          tags: [],
          verify_type: '1',
          add: '',
          xiajia: ''
        },
        tableData: [],
        filter_status_list: [
          {text: "启用", value: "启用"},
          {text: "未使用", value: "未使用"},
          {text: "故障", value: "故障"},
          {text: "下架", value: "下架"},
          {text: "未知", value: "未知"},
        ],
        // 标签
        tag_list: [],
        filter_tag_list: [],
        // 宿主机
        host_machine_list: [],
        //idc
        idc_list: [],
        filter_idc_list: [],
        // 用户
        user_list: [],
        // 左侧选择数据
        Selection: [],
        // 页面配置
        config: {
          page: 1,
          page_size: 10,
          total: undefined,
          select: 'ip',
          search: "",
          showCreateTime: false,
          showKefu: false,
          showOps: false
        }
      }
    },
    methods: {
      getAssetsTableData(event, my_url) {
        if (!my_url) {
          my_url = `api/v1/assets/info/?type=2&page=${this.config.page}&limit=${this.config.page_size}`;
        }
        this.$http.get(my_url)
          .then(resp => {
            this.tableData = resp.data.data;
            this.config.total = resp.data.count;
          }).catch(err => {
          console.log(err)
        })
      },
      getTagData() {
        this.$http.get("api/v1/tag/")
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            resp.data.forEach(tag => {
              this.filter_tag_list.push({text: tag.name, value: tag.name});
              this.tag_list.push({label: tag.name, value: tag.id});
            });
          }).catch(err => {
          console.log(err)
        })
      },
      getIdcData() {
        this.$http.get("api/v1/idc/")
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            resp.data.forEach(idc => {
              this.filter_idc_list.push({text: idc.name, value: idc.name});
              this.idc_list.push({label: idc.name, value: idc.id});
            });
          }).catch(err => {
          console.log(err)
        })
      },
      getAllUserData() {
        this.$http.get("api/v1/user/")
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            resp.data.forEach(user => {
              this.user_list.push({label: user.realname, value: user.id});
            });
          }).catch(err => {
          console.log(err)
        })
      },
      getHostMachineData() {
        this.$http.get("api/v1/assets/?type=1")
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            resp.data.forEach(host => {
              this.host_machine_list.push({label: host.ip, value: host.id})
            })
          }).catch(err => {
          console.log(err)
        })
      },
      assetsAdd() {
        this.operateType = "add";
        this.assets = this.default_assets;
        this.visible = true
      },
      assetsEdit(row) {
        this.$http.get(`api/v1/assets/${row.id}/`)
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.assets = resp.data;
            this.operateType = 'edit';
            this.visible = true
          }).catch(err => {
          this.$alert('未找到该资产,可能由于后台已删除,请刷新！', '错误', {
            confirmButtonText: '确定',
          });
          console.log(err)
        })
      },
      assetsSubmit(obj) {
        // obj 市提交后的数据

        // 如果数据为空，会自动填入null 这里要转换成空字符串
        Object.keys(obj).forEach(key => {
          if (obj[key] === null) {
            obj[key] = "";
          }
        });

        if (this.operateType === 'add') {
          this.$http.post(`api/v1/assets/`, obj, {
            transformRequest: [function (data) {
              let params = "";
              for (let index in data) {
                params += index + "=" + data[index] + "&"
              }
              return params
            }]
          })
            .then(resp => {
              // 需要将 tag id 转换 text/value tag name 转化 value/label
              this.$message({
                message: '恭喜，添加成功！',
                type: 'success'
              });
              this.visible = false;
              // 刷新表格
              this.getAssetsTableData()
            }).catch(err => {
            this.$notify.error({
              title: '错误',
              message: '出错了:' + err.data.message,
              duration: 0
            });
            console.log(err)
          })
        } else {
          this.$http.put(`api/v1/assets/${obj.id}/`, obj, {
            transformRequest: [function (data) {
              let params = "";
              for (let index in data) {
                params += index + "=" + data[index] + "&"
              }
              return params
            }]
          })
            .then(resp => {
              // 需要将 tag id 转换 text/value tag name 转化 value/label
              this.$message({
                message: '恭喜，修改成功！',
                type: 'success'
              });
              this.visible = false;
              // 刷新表格
              this.getAssetsTableData()
            }).catch(err => {
            this.$notify.error({
              title: '错误',
              message: '出错了:' + err.data.message,
              duration: 0
            });
            console.log(err)
          })

        }
      },
      searchAssets() {
        let url = `api/v1/assets/?type=2&${this.config.select}=${this.config.search}`;
        this.getAssetsTableData(undefined, url)
      },
      deleteAssets() {
        // console.log('当前选中', this.Selection)
        let id_list = [];
        this.Selection.forEach(obj => {
          id_list.push(obj.id)
        });
        // 发送delete 请求
        let param = {ids: id_list};
        this.$http.delete("api/v1/assets/", {data: param}, {})
          .then(resp => {
            // 需要将 tag id 转换 text/value tag name 转化 value/label
            this.$message({
              message: '删除成功！',
              type: 'success'
            });
            // 刷新表格
            this.getAssetsTableData()
          }).catch(err => {
          this.$notify.error({
            title: '错误',
            message: '出错了:' + err.data.message,
            duration: 0
          });
          console.log(err)
        })
      },
      assetsInfo(row) {
        let base = [
          {
            path: '/',
            component: () => import('@/views/Main'),
            children: []
          }
        ];
        // 动态添加到路由中
        // 而且顶部tab 菜单需要加入
        let asset = {
          name: row.ip,
          path: "/" + row.ip,
          label: row.ip,
          id: row.id
        };
        // 调用tab vuex的 添加到导航中去
        this.$store.commit("setTab", asset);
        this.$store.commit("setAssetsId", asset);
        // 加入到路由
        asset.component = () => import("@/views/assets/assetsInfo");
        // 动态添加路由
        base[0].children.push(asset);
        this.$router.addRoutes(base);
        // 跳转到刚添加的页面，并给这个路由传参
        this.$router.push({name: row.ip})
      },
      filterTag(value, row) {
        let eg = false;
        row.tags.forEach(tag => {
          if (tag === value) {
            eg = true
          }
        });
        return eg
      },
      filterIdc(value, row) {
        return value === row.idc
      },
      filterStatus(val, row) {
        return val === row.status
      },
      clearFilter() {
        this.$refs.assetsTable.clearFilter();
      },
      // 多选 点击后获得选中数据
      handleSelectionChange(val) {
        this.Selection = val;
      },
      handleSizeChange(val) {
        // console.log(`每页 ${val} 条`);
        this.config.page_size = val;
        this.getAssetsTableData()
      },
      handleCurrentChange(val) {
        // console.log(`当前页: ${val}`);
        this.config.page = val;
        this.getAssetsTableData()
      },
      exportExcel() {
        let wb = XLSX.utils.table_to_book(document.querySelector('.el-table__body'), {raw: true});
        let wbout = XLSX.write(wb, {bookType: 'xlsx', bookSST: true, type: 'array'});
        try {
          FileSaver.saveAs(new Blob([wbout], {type: 'application/octet-stream'}), '虚拟机信息.xlsx')
        } catch (e) {
          if (typeof console !== 'undefined') console.log(e, wbout)
        }
        return wbout
      }
    },
    created() {
      let url = `api/v1/assets/?page=${this.config.page}&limit=${this.config.page_size}`;
      this.getAssetsTableData(url);
      this.getTagData();
      this.getIdcData();
      this.getAllUserData();
      this.getHostMachineData()
    }
  }
</script>
<style lang="scss" scoped>
    .mytab {
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
            height: calc(100% - 35px);
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