import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Vuetify from 'vuetify'
import VueWs from './vue-ws.js'

Vue.use(VueRouter);
Vue.use(Vuetify)
Vue.config.debug = true; Vue.config.devtools = true;

let url = 'ws://' + location.hostname + ':' + location.port + '/ws';
Vue.use(VueWs,url)

import '../node_modules/vuetify/dist/vuetify.css'

import dashboard from './Pages/Dashboard.vue'
import setting from './Pages/Setting.vue'

const routes = [
  {name:'Dashboard',path:'/',component:dashboard},
  {name:'Setting',path:'/setting',component:setting}
];

const router = new VueRouter({
    routes
});

new Vue({
  el: '#app',
  render: h => h(App),
  router:router
})
