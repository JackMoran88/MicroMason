import Vue from 'vue';

import axios from 'axios';
import store from '../index';

export default {
  state: {
    categories: [],
  },
  modules: {},
  actions: {
    GET_CATEGORY_LIST({ commit }) {
      return axios(`${store.state.backendUrlApi}/categories/`,
        {
          method: 'POST',
        })
        .then((resp) => {
          commit('SET_CATEGORY_LIST_TO_STATE', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          return error;
        });
    },

  },
  getters: {
    CATEGORIES: (state) => state.categories,
  },
  mutations: {
    SET_CATEGORY_LIST_TO_STATE: (state, categories) => {
      Vue.set(state, 'categories', categories);
    },
  },
};
