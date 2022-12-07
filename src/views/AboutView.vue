<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
  >
    <el-menu-item index="1"><a href='/'>      <el-icon><House /></el-icon>GPU-RPMA</a></el-menu-item>
    <el-menu-item index="2"><a href='http://10.15.89.84:9999'>   <el-icon><Document /></el-icon>Doc</a></el-menu-item>
    <el-menu-item index="3"><a href='/about'> <el-icon><InfoFilled /></el-icon>About</a></el-menu-item>
    <el-menu-item index="4">
      <a href='https://github.com/wutianyuan1/gpu-rpma'>
      <el-icon>
      <img :style="{width: '20px', height: '20px'}" src="@/assets/github-fill.png"/>
      </el-icon>Github
      </a>
    </el-menu-item>
  </el-menu>
  <div align="center">
    <h1>About GPU-RPMA</h1>
  </div>
  <el-divider border-style="double" />
  <span>GPU-RPMA is an open-source DNN checkpointing system developed by 
    <a href="https://github.com/stevelee477">stevelee477</a> and 
    <a href="https://github.com/wutianyuan1">wutianyuan1</a>. Features of GPU-RPMA include:
  </span>

  <ul>
    <li>Easy-to-deploy</li>
    <li>Zero-copy</li>
    <li>Async-checkpointing</li>
  </ul>

  <h2>Updates</h2>

  <el-table :data="tableData" height="250" style="width: 100%">
    <el-table-column prop="date" label="Date" width="180" />
    <el-table-column prop="update" label="Update Note" />
  </el-table>
</template>

<script>
import { InfoFilled, Document, House } from '@element-plus/icons-vue'

export default {
  data() {
    return {activeIndex: '3',
      tableData: [{date: '2022-12-03', update: 'Add some shit to Pytorch'},
      {date: '2022-12-06', update: 'Add some other shit to Pytorch'}]
    }
  }
}

</script>
  
<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
