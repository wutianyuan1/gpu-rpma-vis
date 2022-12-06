<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
  >
    <el-menu-item index="1"><a href='/'>      <el-icon><House /></el-icon>GPU-RPMA</a></el-menu-item>
    <el-menu-item index="2"><a href='/doc'>   <el-icon><Document /></el-icon>Doc</a></el-menu-item>
    <el-menu-item index="3"><a href='/about'> <el-icon><InfoFilled /></el-icon>About</a></el-menu-item>
    <el-menu-item index="4">
      <a href='https://github.com/wutianyuan1/gpu-rpma'>
      <el-icon>
      <img :style="{width: '20px', height: '20px'}" src="@/assets/github-fill.png"/>
      </el-icon>Github
      </a>
    </el-menu-item>
  </el-menu>
  
  <div class="common-layout">
    <el-container>
      <!-- side bar here -->
      <el-aside width="10%">
        <el-menu default-active="0">
          <el-menu-item><b>Devices</b></el-menu-item>
          <el-menu-item
            :index="item.id + ''"
            v-for="item in devList"
            :key="item.id"
            @click.native="updateDevice(item.id, item.devName)"
          >{{item.devName}}
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!-- main here -->
      <el-main>
        <el-row>
          <el-col :span="12">
            <div id="usageChart" :style="{width: '600px', height: '400px'}"></div>
            <el-table :data="usageTable" style="width: 100%">
            <el-table-column prop="total" label="Total Space" />
            <el-table-column prop="valid" label="Used Space" />
            <el-table-column prop="invalid" label="Invalid Space" />
            <el-table-column prop="free" label="Free Space" />
            </el-table>
            <!-- <div id="usageChart" :style="{width: '100%', height: '50px'}"></div> -->
            <!-- <div align="center"><el-button @click="updateUsage">Refresh PMEM Usage</el-button></div> -->
          </el-col>
          
          <el-col :span="12">
            <!-- model table -->
            <el-table :data="modelTable" height="480px" style="width: 100%">
            <el-table-column type="expand">
              <template #default="props">
                <el-table :data="props.row.detail">
                  <el-table-column prop="detail_name" label="Layer Name" />
                  <el-table-column prop="detail_size" label="Layer Size" />
                </el-table>
              </template>
            </el-table-column>
            <el-table-column prop="name"    label="Model Name" />
            <el-table-column prop="layers"  label="#Layers"/>
            <el-table-column prop="ops"     label="Operations">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="openDialog(scope.$index, scope.row)">Delete</el-button>
                <el-dialog
                  v-model="dialogVisible"
                  title="Tips"
                  width="30%"
                  :before-close="handleClose"
                >
                  <div align="center">
                    <el-icon><img :style="{width: '60px', height: '60px'}" src="@/assets/remove.webp"/></el-icon>
                    <br />
                    <span>你真的要删了{{model_name}}吗，删了可就真的没了！想好了吗喵？</span>
                  </div>
                  <template #footer>
                    <span class="dialog-footer">
                      <el-button @click="dialogVisible = false">Cancel</el-button>
                      <el-button type="primary" @click="deleteModel">
                        Confirm
                      </el-button>
                    </span>
                  </template>
                </el-dialog>
              </template>
            </el-table-column>
            </el-table>
            <!-- update models -->
            <!-- <div id="usageChart" :style="{width: '600px', height: '100px'}"></div>
            <div align="center"><el-button @click="updateModels">Refresh Model Information</el-button></div> -->
          </el-col>
          
          <el-col :span="24">
            <div id="blank1" :style="{width: '600px', height: '50px'}"></div>
          </el-col>

          <!-- operation buttons -->
          <el-col :span="6">
          </el-col>
          <el-col :span="6">
            <div align="center"><el-button @click="updateAll">Refresh PMEM Usage</el-button></div>
          </el-col>
          <el-col :span="6">
            <div align="center">
              <el-button @click="repackVisible = true">Repack PMEM</el-button>
              <el-dialog
                v-model="repackVisible"
                title="Tips"
                width="30%"
                :before-close="closeRepack"
              >
                <div align="center">
                  <el-icon><img :style="{width: '60px', height: '60px'}" src="@/assets/party.webp"/></el-icon>
                  <br />
                  <span>Repack PMEM？想好了吗喵？</span>
                </div>
                <template #footer>
                  <span class="dialog-footer">
                    <el-button @click="closeRepack">Cancel</el-button>
                    <el-button type="primary" @click="repackPM">
                      Confirm
                    </el-button>
                  </span>
                </template>
              </el-dialog>
            </div>
          </el-col>
          <el-col :span="6">
          </el-col>
          <!-- ends here -->
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>


<script>
  import { InfoFilled, Document, House } from '@element-plus/icons-vue'
  import { ElMessageBox } from 'element-plus'
  import axios from 'axios'

  let usageChart = null;

  function GB(x) {
    return (x/(1024*1024*1024)).toFixed(2) + 'GB';
  };

  export default {
    data() {
      return {
        dialogVisible: false,
        repackVisible: false,
        activeIndex: '1',
        modelTable: [
          {name: 'SBBert', layers: 233},
          {name: 'SBBert', layers: 233},
          {name: 'SBBert', layers: 233},
          {name: 'SBBert', layers: 233},
          {name: 'SBBert', layers: 233},
          {name: 'SBBert', layers: 233},
        ],
        usageTable: [
          {total: "0", valid: "0", invalid: "0", free: "0"}
        ],
        piechartData: [{
          name: 'usage',
          type: 'pie',
          radius: '55%',
          data:[{value:0, name:'Valid Checkpoints'}, {value:0, name:'Invalid Checkpoints'}, {value:100, name:'Free Space'}]
        }],
        devList: [{devName:'a', id:0}, {devName:'b', id:1}, {devName:'c', id:2}],
        model_index: 0,
        model_name: "None"
      };
    },
    mounted() {
      usageChart = this.$echarts.init(document.getElementById("usageChart"));
      console.log("init!!!")
      this.initDevice();
      this.updateAll();
      window.onresize = () => {
        usageChart.resize();
      }
    },
    methods: {
      handleSelect(key, keyPath) {

      },
      updateModels() { 
        axios.get('/models/').then(response => {
          var num_models = response.data.models;
          var model_list = response.data.model_list;
          this.$data.modelTable.length = num_models;
          for (var i = 0; i < num_models; i++) {
            this.$data.modelTable[i] = model_list[i];
          }
        })
      },
      deleteModel() {
        var index = this.$data.model_index;
        var minfo = this.$data.modelTable.splice(index, 1);
        var mname = minfo[0].name;
        console.log("remove:", mname);
        axios.post('/deletechkpt/', {'name': mname}).then(response => {
          console.log(response);
        }, error => {
          console.log("error!!!!" + error);
        })
        this.$data.dialogVisible = false;
        this.updateAll();
      },
      updateUsage() {
        axios.get('/pmemusage/').then(response => {
          var num_parts = response.data.num_parts;
          var percentages = response.data.percentages;
          for (var i = 0; i < num_parts; i++) {
            this.$data.piechartData[0].data[i] = percentages[i];
          }
          var total = percentages[0].value + percentages[1].value + percentages[2].value;
          this.$data.usageTable[0].total = GB(total);
          this.$data.usageTable[0].valid = GB(percentages[0].value);
          this.$data.usageTable[0].invalid = GB(percentages[1].value);
          this.$data.usageTable[0].free = GB(percentages[2].value);
          usageChart.setOption({
            title: {text: 'Persistent Memory Usage', left: 'center'},
            series: this.$data.piechartData
          }, true);
        })
      },
      initDevice() {
        axios.get('/getdevs/').then(response => {
          var devices = response.data.devices;
          this.$data.devList.length = devices.length;
          for (var i = 0; i < devices.length; i++) {
            this.$data.devList[i].id = i;
            this.$data.devList[i].devName = devices[i];
          }
        })
      },
      updateDevice(index, row) {
        axios.post('/switchdevice/', {'content': [index, row]}).then(response => {
          console.log(response);
        }, error => {
          console.log("error!!!!" + error);
        })
        // 我也不知道为啥要搞两遍才行。。。
        this.updateAll();
      },
      updateAll() {
        this.updateUsage();
        this.updateModels();
        this.updateUsage();
        this.updateModels();
      },
      openDialog(idx, content) {
        this.$data.model_index = idx;
        this.$data.model_name = content.name;
        this.$data.dialogVisible = true;
      },
      handleClose() {
        this.$data.dialogVisible = false;
      },
      repackPM() {
        axios.post('/repack/').then(response => {
          console.log(response);
        }, error => {
          console.log("error!!!!" + error);
        })
        this.$data.repackVisible = false;
        this.updateAll();
      },
      closeRepack() {
        this.$data.repackVisible = false;
      }
    }
  }
</script>

<style>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs--right .el-tabs__content,
.el-tabs--left .el-tabs__content {
  height: 100%;
}
</style>
