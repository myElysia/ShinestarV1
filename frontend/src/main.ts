import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import locale from "element-plus/es/locale/lang/zh-cn";
import { createPinia } from "pinia";
//国际化

const app = createApp(App)

// 初始化Pinia
const pinia = createPinia()

// 通过 use(router) 挂载路由
app.use(router).use(pinia).use(ElementPlus, { locale }).mount('#app')

// 全局注册图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}