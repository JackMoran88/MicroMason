import Vue from 'vue';

import axios from 'axios';
import store from '../index';

export default {
  state: {
    wish: [],
    wish_ids: []
  },
  modules: {},
  actions: {
    GET_WISH({ commit }, data) {
      store.dispatch('GET_WISH_IDS')
      return axios(`${store.state.backendUrlApi}/wish/detail/`,
        Vue.lodash.merge({
          method: 'GET',
          data: {},
          params: data,
        },
        this._vm.$USER_DATA_REQUEST(),))
        .then((resp) => {
          this._vm.$debug_log('Wish обновлен');
          commit('SET_WISH_TO_STATE', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    GET_WISH_IDS({ commit }) {
      return axios(`${store.state.backendUrlApi}/wish/ids/`,
        Vue.lodash.merge({
          method: 'GET',
          data: {},
        },
        this._vm.$USER_DATA_REQUEST(),))
        .then((resp) => {
          this._vm.$debug_log('Wish обновлен');
          commit('SET_WISH_IDS_TO_STATE', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    ADD_WISH({ commit }, productId) {
      return axios(`${store.state.backendUrlApi}/wish/add/`,
        Vue.lodash.merge({
          method: 'POST',
          data: {
            product: productId,
          },
        },
        this._vm.$USER_DATA_REQUEST(),))
        .then((resp) => {
          this._vm.$debug_log('В wish добавлен товар');
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
        }).finally(() => {
          store.dispatch('GET_WISH');
          store.dispatch('GET_CUSTOMER_DETAIL', store.getters.TOKEN);
        });
    },
    DELETE_WISH({ commit }, productId) {
      return axios(`${store.state.backendUrlApi}/wish/delete/`,
        Vue.lodash.merge({
          method: 'POST',
          data: { product: productId },
        },
        this._vm.$USER_DATA_REQUEST(),))
        .then((resp) => {
          this._vm.$debug_log('Из wish удален товар');
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
        }).finally(() => {
          store.dispatch('GET_WISH');
          store.dispatch('GET_CUSTOMER_DETAIL', store.getters.TOKEN);
        });
    },
  },
  getters: {
    WISH: (state) => state.wish,
    WISH_IDS: (state) => state.wish_ids,
  },
  mutations: {
    SET_WISH_TO_STATE: (state, wish) => {
      Vue.set(state, 'wish', wish);
    },
    SET_WISH_IDS_TO_STATE: (state, data) => {
      Vue.set(state, 'wish_ids', data);
    },
  },
};

// import store from '../index.js'
// import axios from 'axios'
//
//
// export default {
//     state: {
//
//     },
//     modules: {},
//     actions: {
//
//     },
//     getters: {
//
//     },
//     mutations: {
//
//     },
// }

