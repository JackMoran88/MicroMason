import Vue from 'vue';

import axios from 'axios';
import router from '@/router';
import store from '../index';

export default {
  state: {
    server_problem: false,

    shop_settings: [],
    sliders: [],
    sort_types: [],

    page_loaded: false,

    product_search_list: [],
    category_search_list: [],

    loading: false,

  },
  modules: {},
  actions: {
    TEST_CONNECTION({ commit }) {
      return new Promise((resolve, reject) => {
        axios(`${store.state.backendUrlApi}/connection/`,
          { method: 'POST' })
          .then(() => {
            if (router.history.current.fullPath === '/503') {
              this._vm.$debug_log('Перенаправляю с 503 на главную');
              router.replace({ name: 'Home' });
            }

            commit('SET_SERVER_PROBLEM', false);
            resolve();
          })
          .catch(() => {
            commit('SET_SERVER_PROBLEM', true);
            router.replace({ name: 'ServerProblem' })
              .catch(() => {
              });
            reject();
          });
      });
    },

    START({ commit }) {
      store.dispatch('GET_DEVICE_TYPE');
      store.dispatch('TEST_CONNECTION')
        .then(() => {
          store.dispatch('GET_CUSTOMER_DETAIL', store.getters.TOKEN);
          store.dispatch('CHECK_USER').then(() => {
            store.dispatch('GET_WISH');
            store.dispatch('GET_CART_DETAIL');
            store.dispatch('GET_COMPARE_DETAIL');
            store.dispatch('GET_USER_REVIEWS');
          });
          store.dispatch('GET_SHOP_SLIDERS');
          store.dispatch('GET_SHOP_SETTINGS');
          store.dispatch('GET_SORT_TYPES');
          store.dispatch('GET_CATEGORY_LIST');
        });
    },

    GET_SHOP_SETTINGS({ commit }) {
      return axios(`${store.state.backendUrlApi}/settings/`,
        {
          method: 'POST',
        })
        .then((resp) => {
          commit('SET_SHOP_SETTIGNS', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },

    GET_SHOP_SLIDERS({ commit }) {
      return axios(`${store.state.backendUrlApi}/settings/sliders/`,
        {
          method: 'POST',
        })
        .then((resp) => {
          commit('SET_SHOP_SLIDERS', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },

    GET_SORT_TYPES({ commit }) {
      return axios(`${store.state.backendUrlApi}/settings/parameters/`,
        {
          method: 'POST',
        })
        .then((resp) => {
          commit('SET_SORT_TYPES', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },

    GET_PRELOADER({ commit }) {
      return setTimeout(() => {
        commit('SET_PAGE_LOADED');
      }, 400);
    },

    UPDATE_BREADCRUMBS({ commit }, data) {
      router.replace({ query: { ...data.route.query, temp: Date.now() } });
      // router.replace({query: Object.assign({}, data.route.query, {temp: undefined})})
      router.replace({ query: { ...data.route.query } });
    },

    BREADCRUMBS({ commit }, data) {
      function getPath(crumb) {
        let { path } = crumb;
        for (let i = 0, a = Object.entries(data.route.params); i < a.length; i += 1) {
          const b = a[i];
          const key = b[0];
          const
            value = b[1];
          path = path.replace(`:${key}`, value);
        }
        return path;
      }

      function moveBreadCrumbs() {
        const breadcrumbsLine = document.getElementsByClassName('breadcrumb')[0];
        if (breadcrumbsLine) {
          breadcrumbsLine.scrollLeft = breadcrumbsLine.scrollWidth;
        }
      }

      if (data && data.breadcrumbs) {
        data.breadcrumbs.forEach((value) => {
          let crumb = getPath(value);
          crumb = crumb.match(/\/[\w?-]+$/);
          if (crumb && crumb[0]) {
            crumb = crumb[0].slice(1);
            store.dispatch('GET_BREADCRUMBS', crumb)
              .then((response) => {
                if (response) {
                  value.meta.breadcrumb.label = response;
                  store.dispatch('UPDATE_BREADCRUMBS', data);
                  moveBreadCrumbs();
                }
              }).finally(() => {
                moveBreadCrumbs();
              });
          }
        });
      }
      moveBreadCrumbs();
    },

    GET_BREADCRUMBS({ commit }, data) {
      return new Promise((resolve) => {
        axios({
          url: `${store.state.backendUrlApi}/breadcrumbs/`,
          data: {
            breadcrumb: data,
          },
          method: 'POST',
        })
          .then((resp) => {
            resolve(resp.data.name);
            return resp.data.name;
          }).catch((error) => {
            this._vm.$debug_log(error);
            this._vm.$debug_log(error.response);
          });
      });
    },
    GET_PRODUCT_BY_SEARCH_LIST({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/products/search/list/`,
        {
          method: 'POST',
          data,
        })
        .then((resp) => {
          commit('SET_PRODUCT_SEARCH_LIST', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    GET_CATEGORY_BY_SEARCH_LIST({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/category/search/list/`,
        {
          method: 'POST',
          data,
        })
        .then((resp) => {
          commit('SET_CATEGORY_SEARCH_LIST', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },

    NOT_FOUND({ commit }, error) {
      if (error) {
        this._vm.$debug_log(error);

        if (error.response.status === 404) {
          router.replace({ name: 'NotFound' });
        }
      }
    },

  },
  getters: {
    SERVER_PROBLEM: (state) => state.server_problem,
    SETTINGS: (state) => state.shop_settings,
    SLIDERS: (state) => state.sliders,
    SORT_TYPES: (state) => state.sort_types,
    PAGE_LOADED: (state) => state.page_loaded,

    PRODUCT_SEARCH_LIST: (state) => state.product_search_list,
    CATEGORY_SEARCH_LIST: (state) => state.category_search_list,

    LOADING: (state) => state.loading,
  },
  mutations: {
    SET_SERVER_PROBLEM: (state, data) => {
      Vue.set(state, 'server_problem', data);
    },

    SET_SHOP_SETTIGNS: (state, data) => {
      Vue.set(state, 'shop_settings', data[0]);
    },
    SET_SHOP_SLIDERS: (state, data) => {
      Vue.set(state, 'sliders', data);
    },
    SET_SORT_TYPES: (state, data) => {
      Vue.set(state, 'sort_types', data);
    },
    SET_PAGE_LOADED: (state) => {
      Vue.set(state, 'page_loaded', true);
    },
    SET_PRODUCT_SEARCH_LIST: (state, products) => {
      Vue.set(state, 'product_search_list', products);
    },
    CLEAR_PRODUCT_SEARCH_LIST: (state) => {
      Vue.set(state, 'product_search_list', []);
    },
    SET_CATEGORY_SEARCH_LIST: (state, products) => {
      Vue.set(state, 'category_search_list', products);
    },
    CLEAR_CATEGORY_SEARCH_LIST: (state) => {
      Vue.set(state, 'category_search_list', []);
    },
    SET_LOADING: (state, value) => {
      Vue.set(state, 'loading', value);
    },

  },
};
