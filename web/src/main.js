import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import ElementUI from 'element-ui'
// import 'element-ui/lib/theme-chalk/index.css';
import '../theme/index.css'
import '@/assets/scss/reset.scss'
import http from '@/api/config'

Vue.use(ElementUI);
Vue.prototype.$http = http;
Vue.config.productionTip = false;

router.beforeEach((to, form, next) => {
  store.commit('getToken');
  let token = store.state.user.token;
  if (!token && to.name !== 'login') {
    // 未登录用户要跳转到登录
    next({name: 'login'})
  } else {
    next()
  }
});

new Vue({
  router,
  store,
  render: h => h(App),
  created() {
    store.commit("getToken");
    store.commit("MenuToRouter", router);
    store.commit("getUser");
    // 刷新后跳转到 主页
  }
}).$mount('#app');
