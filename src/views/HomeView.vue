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
            <div id="myChart" :style="{width: '600px', height: '400px'}"></div>
            <el-table :data="usageTable" style="width: 100%">
            <el-table-column fixed prop="total" label="Total Space" />
            <el-table-column fixed prop="valid" label="Used Space" />
            <el-table-column fixed prop="invalid" label="Invalid Space" />
            <el-table-column fixed prop="free" label="Free Space" />
            </el-table>
            <div id="myChart" :style="{width: '100%', height: '50px'}"></div>
            <div align="center"><el-button @click="updateUsage">Refresh PMEM Usage</el-button></div>
          </el-col>
          
          <el-col :span="12">
            <!-- model table -->
            <el-table :data="modelTable" style="width: 100%">
            <el-table-column fixed prop="name" label="Model Name" />
            <el-table-column prop="layers" label="#Layers"/>
            <el-table-column fixed="right" prop="ops" label="Operations">
              <template #default>
                <el-button link type="primary" size="small" @click="viewDetail">View Details</el-button>
                <el-button link type="primary" size="small" @click="deleteModel">Delete</el-button>
              </template>
            </el-table-column>
            </el-table>
            <!-- update models -->
            <div id="myChart" :style="{width: '600px', height: '100px'}"></div>
            <div align="center"><el-button @click="updateModels">Refresh Model Information</el-button></div>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>


<script>
  import { InfoFilled, Document, House } from '@element-plus/icons-vue'
  import { ref } from 'vue'
  import axios from 'axios'
  let myChart = null;

  function GB(x) {
    return (x/(1024*1024*1024)).toFixed(2) + 'GB';
  };

  export default {
    data() {
      return {
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
      };
    },
    mounted() {
      myChart = this.$echarts.init(document.getElementById("myChart"));
      console.log("init!!!")
      this.initDevice();
      this.updateUsage();
      this.updateModels();
      window.onresize = () => {
        myChart.resize();
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
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
      viewDetail() {

      },
      deleteModel() {

      },
      updateUsage() {
        console.log("update usage!");
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
          myChart.setOption({
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
        // TODO: get PMEM device by name
        console.log("!!!!afsdfda", index, row);
        axios.post('/switchdevice/', {'content': [index, row]}).then(response => {
          console.log(response);
        }, error => {
          console.log("error!!!!" + error);
        })
        // 我也不知道为啥要搞两遍才行。。。
        this.updateUsage();
        this.updateModels();
        this.updateUsage();
        this.updateModels();
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
