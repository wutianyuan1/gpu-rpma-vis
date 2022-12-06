import { createApp, VueElement } from 'vue'
import * as echarts from 'echarts'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = 'http://10.15.89.84:8000';

const app = createApp(App);
app.config.globalProperties.$echarts = echarts;

app.use(ElementPlus);
app.use(router);
app.mount('#app');
