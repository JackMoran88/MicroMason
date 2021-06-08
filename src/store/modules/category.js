import Vue from 'vue';

import axios from 'axios';
import store from '../index';

export default {
  state: {
    categories: {
      queryset: [],
      load: false,
    },
  },
  modules: {},
  actions: {
    GET_CATEGORY_LIST({ commit }) {
      return axios(`${store.state.backendUrlApi}/categories/`,
        {
          method: 'GET',
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
      Vue.set(state.categories, 'queryset', categories);
      Vue.set(state.categories, 'load', true);
      // localStorage.setItem('categories', JSON.stringify(state.categories))
    },
  },
};
