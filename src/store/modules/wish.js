import Vue from 'vue';

import axios from 'axios';
import store from '../index';

export default {
  state: {
    wish: [],
  },
  modules: {},
  actions: {
    GET_WISH({ commit }) {
      return axios(`${store.state.backendUrlApi}/wish/detail/`,
        window._.merge({
          method: 'POST',
          data: {},
        },
        store.getters.USER_DATA_REQUEST))
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
    ADD_WISH({ commit }, productId) {
      return axios(`${store.state.backendUrlApi}/wish/add/`,
        window._.merge({
          method: 'POST',
          data: {
            product: productId,
          },
        },
        store.getters.USER_DATA_REQUEST))
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
        window._.merge({
          method: 'POST',
          data: { product: productId },
        },
        store.getters.USER_DATA_REQUEST))
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
  },
  getters: {
    WISH: (state) => state.wish,
    WISH_IDS: (state) => {
      if (state.wish) {
        return state.wish.map((value) => value.id);
      }
      return [];
    },

  },
  mutations: {
    SET_WISH_TO_STATE: (state, wish) => {
      Vue.set(state, 'wish', wish);
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
