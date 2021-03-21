import Vue from 'vue';
import axios from 'axios';
import store from '../index';

export default {
  state: {
    product: [],
    slides: [],
    products: [],

    products_last: [],

    filters: [],

    comments: [],
  },
  modules: {},
  actions: {
    SET_PRODUCT_SLIDES({ commit }) {
      const slides = [];
      let slide = {
        src: store.state.backendUrl + store.getters.PRODUCT.main_image.gallery,
        thumb: store.state.backendUrl + store.getters.PRODUCT.main_image.gallery,
      };
      if (store.getters.PRODUCT.images) {
        store.getters.PRODUCT.images.forEach((value) => {
          slide = {
            src: store.state.backendUrl + value.image.gallery,
            thumb: store.state.backendUrl + value.image.gallery,
          };
          slides.unshift(slide);
        });
      }
      slides.unshift(slide);
      commit('SET_SLIDES_TO_STATE', slides);
      return slides;
    },
    GET_PRODUCT({ commit }, slug) {
      return axios(`${store.state.backendUrlApi}/product/`,
        {
          method: 'POST',
          data: {
            slug,
          },
        })
        .then((resp) => {
          commit('SET_PRODUCT_TO_STATE', resp.data);
          store.dispatch('SET_PRODUCT_SLIDES');
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          store.dispatch('NOT_FOUND', error);
          return error;
        });
    },
    GET_FILTERS({ commit }, slug) {
      return axios(`${store.state.backendUrlApi}/category/detail/`,
        {
          method: 'POST',
          data: {
            slug,
          },
        })
        .then((resp) => {
          commit('SET_FILTERS_TO_STATE', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          store.dispatch('NOT_FOUND', error);
          return error;
        });
    },

    GET_PRODUCT_BY_ID({ commit }, id) {
      return axios(`${store.state.backendUrlApi}/product/`,
        {
          method: 'POST',
          data: {
            id,
          },
        })
        .then((resp) => {
          commit('SET_PRODUCT_TO_STATE', resp.data);
          store.dispatch('SET_PRODUCT_SLIDES');
          return resp.data;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.responce);
          return error;
        });
    },

    GET_PRODUCT_LAST({ commit }, count) {
      return axios(`${store.state.backendUrlApi}/products/last/${count ? `?count=${count}` : ''}`,
        {
          method: 'GET',
        })
        .then((resp) => {
          commit('SET_PRODUCT_LAST_TO_STATE', resp.data)
          return resp.data;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.responce);
          return error;
        });
    },

    GET_PRODUCTS_BY_IDS({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/products/`,
        {
          method: 'POST',
          data: {
            ids: data,
          },
        })
        .then((resp) =>
          resp.data)
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },

    GET_PRODUCTS({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/category/products/`+
      `${data.filters ? `${data.filters}` : ''}`,
      {
        method: 'POST',
        data,
      })
        .then((resp) => {
          commit('SET_PRODUCTS_TO_STATE', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          store.dispatch('NOT_FOUND', error);
          return error;
        });
    },

    GET_PRODUCT_BY_SEARCH({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/products/search/detail/`,
        {
          method: 'POST',
          data,
        })
        .then((resp) => {
          commit('SET_PRODUCTS_TO_STATE', resp.data);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },

    SEND_COMMENT({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/review/add/`,
        {
          method: 'POST',
          data,
        })
        .then((resp) => {
          this._vm.$debug_log('Коментраий отправлен');
          store.dispatch('GET_COMMENTS', data.product);
          store.dispatch('GET_USER_REVIEWS');
          store.dispatch('GET_PRODUCT', store.getters.PRODUCT.slug)
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    SEND_ANSWER({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/review/answer/`,
        {
          method: 'POST',
          data,
        })
        .then((resp) => {
          store.dispatch('GET_COMMENTS', data.product);
          store.dispatch('GET_USER_REVIEWS');
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    DELETE_COMMENT({ commit }, data) {
      return axios(`${store.state.backendUrlApi}/review/delete/`,
        {
          method: 'POST',
          data,
        })
        .then((resp) => {
          store.dispatch('GET_COMMENTS', data.product);
          store.dispatch('GET_USER_REVIEWS');
          store.dispatch('GET_PRODUCT', store.getters.PRODUCT.slug)
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    GET_COMMENTS({ commit }, id) {
      if (id.id) id = id.id;
      return axios(`${store.state.backendUrlApi}/review/detail/`,
        {
          method: 'POST',
          data: {
            id,
          },
        })
        .then((resp) => {
          commit('SET_COMMENTS_TO_STATE', resp.data);
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
    PRODUCT: (state) => state.product,
    PRODUCTS_LAST: (state) => state.products_last,
    PRODUCT_SLIDES: (state) => state.slides,
    PRODUCTS: (state) => state.products,
    COMMENTS: (state) => state.comments,

    FILTERS: (state) => state.filters,
  },
  mutations: {
    SET_PRODUCT_TO_STATE: (state, product) => {
      Vue.set(state, 'product', product);
    },
    SET_PRODUCT_LAST_TO_STATE: (state, product) => {
      Vue.set(state, 'products_last', product);
    },
    SET_SLIDES_TO_STATE: (state, slides) => {
      Vue.set(state, 'slides', slides);
    },
    SET_PRODUCTS_TO_STATE: (state, products) => {
      Vue.set(state, 'products', products);
    },

    SET_FILTERS_TO_STATE: (state, filters) => {
      Vue.set(state, 'filters', filters);
    },

    SET_COMMENTS_TO_STATE: (state, comments) => {
      Vue.set(state, 'comments', comments);
    },
    CLEAR_FILTERS:(state)=>{
       Vue.set(state, 'filters', []);
    }
  },
};
