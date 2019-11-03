import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router';

import HomeComponent from './components/HomeComponent';

Vue.config.productionTip = false

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeComponent
  }
]

const router = new VueRouter({
  routes,
  mode: 'history'
});

new Vue({
  render: h => h(App),
  router,
}).$mount('#app')
