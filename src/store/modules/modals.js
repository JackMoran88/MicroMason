import Vue from 'vue';

export default {
  state: {
    quick_view: {
      state: false,
      ProductSlug: null,
    },
  },
  modules: {},
  actions: {
    SHOW_QUICK_VIEW({ commit }, ProductSlug) {
      commit('S_QUICK_VIEW', ProductSlug);
    },
    CLOSE_QUICK_VIEW({ commit }) {
      commit('C_QUICK_VIEW');
    },
  },
  getters: {
    IS_QUICK_VIEW: (state) => state.quick_view.state,
    QUICK_VIEW: (state) => state.quick_view,
  },
  mutations: {
    S_QUICK_VIEW: (state, ProductSlug) => {
      Vue.set(state.quick_view, 'state', true);
      Vue.set(state.quick_view, 'ProductSlug', ProductSlug);
    },
    C_QUICK_VIEW: (state) => {
      Vue.set(state.quick_view, 'state', false);
      Vue.set(state.quick_view, 'ProductSlug', null);
    },
  },
};
