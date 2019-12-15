<template>
    <div>
        <el-row>
            <el-col :span="11" style="margin: 10px;" :offset="2">
                <el-card class="box-card">
                    <div slot="header">
                        <span>基础信息</span>
                    </div>
                    <el-table border :data="tableData">
                        <el-table-column
                                prop="ip"
                                label="IP">
                        </el-table-column>
                        <el-table-column
                                prop="system"
                                label="系统类型">
                        </el-table-column>
                        <el-table-column
                                prop="asset_type"
                                label="资产类型">
                        </el-table-column>
                        <el-table-column
                                prop="status"
                                label="资产状态">
                        </el-table-column>
                    </el-table>
                    <el-table border :data="tableData">
                        <el-table-column
                                prop="idc"
                                label="机房">
                        </el-table-column>
                        <el-table-column
                                prop="host_machine"
                                label="宿主机">
                        </el-table-column>
                        <el-table-column
                                prop="ftp_port"
                                label="FTP端口">
                        </el-table-column>
                    </el-table>
                    <el-table border :data="tableData">
                        <el-table-column
                                prop="remark"
                                label="备注">
                        </el-table-column>
                        <el-table-column prop="tags" label="标签">
                            <template slot-scope="scope">
                                <el-tag style="margin-right: 3px;" size="mini" v-for="tag in scope.row.tags" :key="tag"
                                        effect="dark" type="info">
                                    {{tag}}
                                </el-tag>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
            <el-col :span="11" style="margin: 10px;">
                <el-card class="box-card">
                    <div slot="header">
                        <span>SSH信息</span>
                    </div>
                    <el-table border :data="tableData">
                        <el-table-column
                                prop="sshuser"
                                label="SSH User">
                        </el-table-column>
                        <el-table-column
                                label="SSH Port"
                                prop="sshport">
                        </el-table-column>
                    </el-table>
                    <el-table border :data="tableData">
                        <el-table-column
                                prop="verify_type"
                                label="验证类型">
                        </el-table-column>
                        <el-table-column
                                label="SSH 密码"
                                prop="sshpwd">
                        </el-table-column>
                        <el-table-column
                                prop="yubico"
                                label="Yubico">
                        </el-table-column>
                        <el-table-column
                                prop="key"
                                label="密匙路径">
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="11" style="margin: 10px;">
                <el-card class="box-card">
                    <div slot="header">
                        <span>MYSQL信息</span>
                    </div>
                    <el-table border :data="tableData">
                        <el-table-column
                                prop="mysql_user"
                                label="MYSQL用户" width="150">
                        </el-table-column>
                        <el-table-column
                                prop="mysql_pwd"
                                label="MYSQL密码">
                        </el-table-column>
                        <el-table-column
                                prop="mysql_port"
                                label="MYSQL端口">
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
  export default {
    name: "InfoCard",
    props: {
      tableData: Array
    }
  }
</script>

<style scoped>

</style>