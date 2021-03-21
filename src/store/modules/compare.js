import Vue from 'vue';

import axios from 'axios';
import store from '../index';

export default {
  state: {
    compare: [],
    compare_ids: [],
  },
  modules: {},
  actions: {
    GET_COMPARE_DETAIL({ commit }) {
      return new Promise((resolve, reject) => axios(`${store.state.backendUrlApi}/compare/list/`,
        window._.merge(
          { method: 'POST' },
          store.getters.USER_DATA_REQUEST,
        ))
        .then((resp) => {
          this._vm.$debug_log('Compare обновлен');
          commit('SET_COMPARE_TO_STATE', resp.data);
          resolve(resp);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          reject(error);
          return error;
        }));
    },
    ADD_TO_COMPARE({ commit }, productId) {
      return axios(`${store.state.backendUrlApi}/compare/add/`,
        window._.merge({
          method: 'POST',
          data: {
            product: productId,
          },
        },
        store.getters.USER_DATA_REQUEST))
        .then(() => {
          this._vm.$debug_log('В compare добавлен товар');
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
        }).finally(() => {
          store.dispatch('GET_COMPARE_DETAIL');
          store.dispatch('GET_CUSTOMER_DETAIL', store.getters.TOKEN);
        });
    },
    DELETE_FROM_COMPARE({ commit }, productId) {
      return axios(`${store.state.backendUrlApi}/compare/delete/`,
        window._.merge({
          method: 'POST',
          data: {
            product: productId,
          },
        },
        store.getters.USER_DATA_REQUEST))
        .then(() => {
          this._vm.$debug_log('В compare добавлен товар');
        })
        .catch((error) => {
          this._vm.$debug_log(error);
        }).finally(() => {
          store.dispatch('GET_COMPARE_DETAIL');
          store.dispatch('GET_CUSTOMER_DETAIL', store.getters.TOKEN);
        });
    },
  },
  getters: {
    COMPARE: (state) => state.compare,
    COMPARE_IDS: (state) => state.compare_ids,
  },
  mutations: {
    SET_COMPARE_TO_STATE: (state, compare) => {
      Vue.set(state, 'compare', compare);
      Vue.set(state, 'compare_ids', state.compare.map((value) => value.product.id));
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
