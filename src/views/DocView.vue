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

  <div align="center">
    <h1>GPU-RPMA Documentation</h1>
  </div>
  <el-divider border-style="double" />
  <span>这是我们糊的一坨屎（但不论如何它不想叫Portus），你tm还想要doc？想得美哦（x</span>
  <el-divider border-style="double" />
  <span>你说得对，但是<a href="https://ys.mihoyo.com/">《原神》</a>是由米哈游自主研发的一款全新开放世界冒险游戏。游戏发生在一个被称作「提瓦特」的幻想世界,在这里,被神选中的人将被授予「神之眼」,导引元素之力。你将扮演一位名为「旅行者」的神秘角色,在自由的旅行中邂逅性格各异、能力独特的同伴们,和他们一起击败强敌,找回失散的亲人——同时,逐步发掘「原神」的真相。</span>
</template>

<script>
import { InfoFilled, Document, House } from '@element-plus/icons-vue'

export default {
  data() {
    return {activeIndex: '2'}
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