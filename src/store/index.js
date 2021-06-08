import Vue from 'vue';
import Vuex from 'vuex';

import product from './modules/product';
import wish from './modules/wish';
import user from './modules/user';
import category from './modules/category';
import ws from './modules/ws';
import cart from './modules/cart';
import shop from './modules/shop';
import setting from './modules/setting';
import modals from './modules/modals';
import order from './modules/order';
import compare from './modules/compare';
import webSocket from './modules/webSocket';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    backendIp: process.env.VUE_APP_BACKEND_IP,
    backendUrlApi: process.env.VUE_APP_BACKEND_URL_API,
    backendUrl: process.env.VUE_APP_BACKEND_URL,
    debug: true,
  },
  mutations: {},
  modules: {
    product,
    wish,
    user,
    category,
    ws,
    cart,
    shop,
    setting,
    modals,
    order,
    compare,
    webSocket
  },
  getters: {
    SERVER_IP: (state) => state.backendIp,
    getServerUrlApi: (state) => state.backendUrlApi,
    getServerUrl: (state) => state.backendUrl,
    DEBUG: (state) => state.debug,
  },
  actions: {},

});
