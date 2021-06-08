import Vue from 'vue';

import axios from 'axios';
import store from '../index';

export default {
  state: {
    orders: [],
    address: [],
    shipping: [],
    payment: [],
    checkoutData: {
      payment: '',
      shipping: '',
      address: '',
      note: '',
      branch: '',
    },
    receipt: [],
  },
  modules: {},
  actions: {
    GET_ORDERS({commit}) {
      return axios(`${store.state.backendUrlApi}/order/list/`,
        Vue.lodash.merge(
          {method: 'GET'},
          this._vm.$USER_DATA_REQUEST(),
        ))
        .then((response) => {
          commit('ORDERS_TO_STATE', response.data);
          return response;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    GET_ADDRESS({commit}) {
      return axios(`${store.state.backendUrlApi}/address/detail/`,
        Vue.lodash.merge(
          {
            method: 'GET',
          },
          this._vm.$USER_DATA_REQUEST(),
        ))
        .then((response) => {
          commit('ADDRESS_TO_STATE', response.data);
          return response;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    GET_SHIPPING({commit}) {
      return axios(`${store.state.backendUrlApi}/shipping/list/`,
        Vue.lodash.merge(
          {method: 'GET'},
          this._vm.$USER_DATA_REQUEST(),
        ))
        .then((response) => {
          commit('SHIPPING_TO_STATE', response.data);
          return response;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    GET_PAYMENT({commit}) {
      return axios(`${store.state.backendUrlApi}/payment/list/`,
        Vue.lodash.merge(
          {method: 'GET'},
          this._vm.$USER_DATA_REQUEST(),
        ))
        .then((response) => {
          commit('PAYMENT_TO_STATE', response.data);
          return response;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    CREATE_ADDRESS({commit}, data) {
      return axios(`${store.state.backendUrlApi}/address/add/`,
        Vue.lodash.merge(
          {
            method: 'POST',
            data,
          },
          this._vm.$USER_DATA_REQUEST(),
        ))
        .then((response) => {
          store.dispatch('GET_ADDRESS');
          return response;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    DELETE_ADDRESS({commit}, id) {
      return axios(`${store.state.backendUrlApi}/address/delete/`,
        Vue.lodash.merge(
          {
            method: 'POST',
            data: {
              id,
            },
          },
          this._vm.$USER_DATA_REQUEST(),
        ))
        .then((response) => {
          store.dispatch('GET_ADDRESS');
          return response;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },

    GET_LIQPAY_DATA({commit}, order_id) {
      return new Promise((resolve, reject) => {
        return axios(`${store.state.backendUrlApi}/order/pay/`,
          Vue.lodash.merge(
            {
              method: 'POST',
              data: {
                order_id,
              },
            },
            this._vm.$USER_DATA_REQUEST(),
          ))
          .then((response) => {
            resolve(response.data)
          })
          .catch((error) => {
            this._vm.$debug_log(error);
            this._vm.$debug_log(error.response);
            return error;
          });
      })
    },

    MAKE_ORDER({commit}) {
      return new Promise((resolve, reject) => {
        axios(`${store.state.backendUrlApi}/order/add/`,
          Vue.lodash.merge(
            {
              method: 'POST',
              data: store.getters.CHECKOUT,
            },
            this._vm.$USER_DATA_REQUEST(),
          ))
          .then((response) => {
            this._vm.$debug_log('Заказ оформлен');
            commit('RECEIPT_TO_STATE', response.data);
            resolve();
            return response;
          })
          .catch((error) => {
            this._vm.$debug_log(error);
            this._vm.$debug_log(error.response);
            reject();
            return error;
          });
      });
    },

    GET_CITY_BY_QUERY({commit}, query) {
      delete axios.defaults.headers.common.Authorization;
      return new Promise((resolve, reject) => {
        axios(`https://api.novaposhta.ua/v2.0/json/`,
          {
            method: 'POST',
            data: {
              "apiKey": "9f114041505c633de9523ec691981d44",
              "modelName": "Address",
              "calledMethod": "searchSettlements",
              "methodProperties": {
                "CityName": query,
                "Limit": "5"
              }
            }
          },
        )
          .then((response) => {
            this._vm.$debug_log(response);
            if (response.data.success === true) {
              resolve(response.data);
              return response;
            }

          }).finally(() => {
          commit('SET_TOKEN_TO_HEADERS')
        })
      });
    },
    GET_BRANCH_BY_QUERY({commit}, query) {
      return new Promise((resolve, reject) => {
        axios(`${store.state.backendUrlApi}/novaposhta/search/`,
          Vue.lodash.merge(
            {
              method: 'POST',
              data: {
                query: query
              }
            },
            this._vm.$USER_DATA_REQUEST(),
          ))
          .then((response) => {
            resolve(response.data);
            return response;
          })
          .catch((error) => {
            this._vm.$debug_log(error);
            this._vm.$debug_log(error.response);
            reject();
            return error;
          });
      });
    },

  },
  getters: {
    ORDERS: (state) => state.orders,
    ADDRESS: (state) => state.address,
    SHIPPING: (state) => state.shipping,
    PAYMENT: (state) => state.payment,
    CHECKOUT: (state) => state.checkoutData,
    RECEIPT: (state) => state.receipt,
  },
  mutations: {
    SET_CHECKOUT_PAYMENT: (state, value) => {
      Vue.set(state.checkoutData, 'payment', value);
    },
    SET_CHECKOUT_SHIPPING: (state, value) => {
      Vue.set(state.checkoutData, 'shipping', value);
    },
    SET_CHECKOUT_ADDRESS: (state, value) => {
      Vue.set(state.checkoutData, 'address', value);
    },
    SET_CHECKOUT_BRANCH: (state, value) => {
      Vue.set(state.checkoutData, 'branch', value);
    },

    CLEAR_CHECKOUT: (state, value) => {
      Vue.set(state.checkoutData, 'payment', '');
      Vue.set(state.checkoutData, 'shipping', '');
      Vue.set(state.checkoutData, 'address', '');
      Vue.set(state.checkoutData, 'note', '');
      Vue.set(state.checkoutData, 'branch', '');
    },

    SET_CHECKOUT_NOTE: (state, value) => {
      Vue.set(state.checkoutData, 'note', value);
    },
    ORDERS_TO_STATE: (state, orders) => {
      Vue.set(state, 'orders', orders);
    },
    ADDRESS_TO_STATE: (state, address) => {
      Vue.set(state, 'address', address);
    },
    SHIPPING_TO_STATE: (state, shipping) => {
      Vue.set(state, 'shipping', shipping);
    },
    PAYMENT_TO_STATE: (state, payment) => {
      Vue.set(state, 'payment', payment);
    },
    RECEIPT_TO_STATE: (state, receipt) => {
      Vue.set(state, 'receipt', receipt);
    },
  },
};
