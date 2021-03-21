import Vue from 'vue';
import store from '../index';

export default {
  state: {
    isMobile: true,
    isDesktop: false,
  },
  modules: {},
  actions: {

    GET_DEVICE_TYPE({ commit }) {
      function deviceSwitch() {
        if (window.innerWidth > 992) {
          store.dispatch('SET_DESKTOP');
        } else {
          store.dispatch('SET_MOBILE');
        }
      }

      window.addEventListener('load', deviceSwitch);
      window.addEventListener('resize', deviceSwitch);
    },

    SET_MOBILE({ commit }) {
      commit('SWITCH_MOBILE');
    },
    SET_DESKTOP({ commit }) {
      commit('SWITCH_DESKTOP');
    },

  },
  getters: {
    IS_MOBILE: (state) => state.isMobile,
    IS_DESKTOP: (state) => state.isDesktop,
  },
  mutations: {
    SWITCH_MOBILE: (state) => {
      Vue.set(state, 'isDesktop', false);
      Vue.set(state, 'isMobile', true);
    },
    SWITCH_DESKTOP: (state) => {
      Vue.set(state, 'isDesktop', true);
      Vue.set(state, 'isMobile', false);
    },
  },
};
