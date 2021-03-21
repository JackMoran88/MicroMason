import Vue from 'vue';

import axios from 'axios';
import store from '../index';

export default {
  state: {
    cart: [],
    cart_ids: [],
  },
  modules: {},
  actions: {
    GET_CART_DETAIL({ commit }) {
      return axios(`${store.state.backendUrlApi}/cart/detail/`,
        window._.merge({
          method: 'POST',
          data: {},
        },
        store.getters.USER_DATA_REQUEST))
        .then((resp) => {
          commit('SET_CART_TO_STATE', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    ADD_TO_CART({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/cart/add/`,
        window._.merge({
          method: 'POST',
          data,
        },
        store.getters.USER_DATA_REQUEST))
        .then((resp) => {
          store.dispatch('GET_CART_DETAIL');
          this._vm.$debug_log('Товар добавлен в корзину');
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    DELETE_FROM_CART({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/cart/delete/`,
        window._.merge({
          method: 'POST',
          data,
        },
        store.getters.USER_DATA_REQUEST))
        .then((resp) => {
          store.dispatch('GET_CART_DETAIL');
          this._vm.$debug_log('Товар удален из корзины');
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
  },
  getters: {
    CART: (state) => state.cart,
    CART_IDS: (state) => state.cart_ids,
  },
  mutations: {
    SET_CART_TO_STATE: (state, cart) => {
      Vue.set(state, 'cart', cart);
      Vue.set(state, 'cart_ids', []);

      state.cart.forEach((value, index) => {
        Vue.set(state.cart_ids, index, value.id);
      });
    },
  },
};
