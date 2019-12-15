<template>
    <el-dialog :title="operateType === 'add' ? '录入资产' : '修改资产'" :visible.sync="visible" fullscreen
               close-on-press-escape center :before-close="dialogClose">
        <el-form ref="assetsForm" :model="assets" :rules="rules" label-width="100px">
            <el-divider content-position="center">基础信息</el-divider>
            <el-row type="fiex" justify="space-between">
                <el-col :span="6">
                    <el-form-item label="IP" prop="ip">
                        <el-input v-model="assets.ip"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="MAC" prop="mac">
                        <el-input v-model="assets.mac"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="系统类型" prop="system">
                        <el-input v-model="assets.system"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="登录账户" prop="sshuser">
                        <el-input v-model="assets.sshuser"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row type="fiex">
                <el-col :span="6">
                    <el-form-item label="资产类型" prop="asset_type">
                        <el-select v-model="assets.asset_type" placeholder="请选择资产类型">
                            <el-option label="物理机" value="1"></el-option>
                            <el-option label="虚拟机" value="2"></el-option>
                            <el-option label="Docker" value="3"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="资产状态" prop="status">
                        <el-select v-model="assets.status" placeholder="请选择资产状态">
                            <el-option label="下架" value="0"></el-option>
                            <el-option label=启用 value="1"></el-option>
                            <el-option label="故障" value="2"></el-option>
                            <el-option label="未使用" value="3"></el-option>
                            <el-option label="未知" value="4"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-divider content-position="center">验证信息</el-divider>
            <el-row type="fiex">
                <el-col :span="6">
                    <el-form-item label="验证类型" prop="verify_type">
                        <el-select v-model="assets.verify_type">
                            <el-option value="0" label="password"></el-option>
                            <el-option value="1" label="key"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="SSH密码" prop="sshpwd" v-show="assets.verify_type === '0' || assets.sshpwd">
                        <el-input v-model="assets.sshpwd"></el-input>
                    </el-form-item>
                    <el-form-item label="密匙路径" v-show="assets.verify_type === '1' || assets.sshkey">
                        <el-input v-model="assets.sshkey"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-divider content-position="center">数据库信息</el-divider>
            <el-row type="fiex">
                <el-col :span="6">
                    <el-form-item label="MYSQL账户">
                        <el-input v-model="assets.mysql_user"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="MYSQL密码">
                        <el-input v-model="assets.mysql_pwd"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="MYSQL端口">
                        <el-input v-model="assets.mysql_port"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-divider content-position="center">其他信息</el-divider>
            <el-row type="fiex">
                <el-col :span="6">
                    <el-form-item label="FTP端口">
                        <el-input v-model="assets.ftp_port"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
            <!--                其他信息-->
            <el-divider content-position="center">关联信息</el-divider>
            <el-row type="fiex">
                <el-col :span="6">
                    <el-form-item label="上架时间">
                        <el-date-picker
                                v-model="assets.add"
                                type="datetime"
                                placeholder="选择日期时间"
                                default-time="12:00:00">
                        </el-date-picker>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="下架时间">
                        <el-date-picker
                                v-model="assets.xiajia"
                                type="datetime"
                                placeholder="选择日期时间"
                                default-time="12:00:00">
                        </el-date-picker>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="标签">
                        <el-select v-model="assets.tags" filterable multiple placeholder="请选择">
                            <el-option
                                    v-for="item in tag_list"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row type="fiex">
                <el-col :span="6">
                    <el-form-item label="宿主机">
                        <el-select v-model="assets.host_machine" filterable placeholder="请选择">
                            <el-option label="----" value="" key="kong"></el-option>
                            <el-option
                                    v-for="item in host_machine_list"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="机房">
                        <el-select v-model="assets.idc" filterable placeholder="请选择">
                            <el-option label="----" value="" key="kong"></el-option>
                            <el-option
                                    v-for="item in idc_list"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="客服">
                        <el-select v-model="assets.user" filterable placeholder="请选择">
                            <el-option label="----" value="" key="kong"></el-option>
                            <el-option
                                    v-for="item in user_list"
                                    :key="item.label +'u'"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="6">
                    <el-form-item label="运维">
                        <el-select v-model="assets.opsuser" filterable placeholder="请选择">
                            <el-option label="----" value="" key="kong"></el-option>
                            <el-option
                                    v-for="item in user_list"
                                    :key="item.label+'yw'"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form-item label="备注">
                        <el-input type="textarea" v-model="assets.remark"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
        <span slot="footer">
                <el-button type="primary" @click="Submit('assetsForm')">提交</el-button>
                <el-button @click="dialogClose">取消</el-button>
            </span>
    </el-dialog>
</template>

<script>
  export default {
    name: "AssetsForm",
    props: {
      assets: Object,
      tag_list: {
        type: Array,
        default: () => {
          return []
        }
      },
      idc_list: {
        type: Array,
        default: () => {
          return []
        }
      },
      user_list: {
        type: Array,
        default: () => {
          return []
        }
      },
      host_machine_list: {
        type: Array,
        default: () => {
          return []
        }
      },
      visible: Boolean,
      operateType: String,
    },
    data() {
      return {
        rules: {
          ip: [
            {required: true, message: '请输入IP', trigger: 'blur'}
          ],
          system: [
            {required: true, message: '请输入系统类型', trigger: 'blur'}
          ],
          sshuser: [
            {required: true, message: '请输入登录账户', trigger: 'blur'}
          ],
          asset_type: [
            {required: true, message: '请选择资产类型', trigger: 'change'}
          ],
          status: [
            {required: true, message: '请选择资产状态', trigger: 'change'}
          ],
        }
      }
    },
    methods: {
      dialogClose(done = undefined) {
        this.$emit("dialogClose")
      },
      Submit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {

            this.$confirm('确定要提交吗, 是否继续?', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              this.$emit("assetsSubmit", this.assets)
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '已取消提交'
              });
            });

          } else {
            this.$alert('提交失败，请填写必要项', '失败', {
              confirmButtonText: '确定'
            });
            return false;
          }
        })
      },
    },
  }
</script>

<style scoped>

</style>