import Vue from 'vue';

import axios from 'axios';
import store from '../index';

export default {
  state: {
    status: '',
    token: localStorage.getItem('token') || sessionStorage.getItem('token') || '',
    token_type: localStorage.getItem('token_type') || sessionStorage.getItem('token_type') || 'Token',
    user: JSON.parse(sessionStorage.getItem('user')) || '',
    anonymous: JSON.parse(sessionStorage.getItem('anonymous')),

    viewed_ids: JSON.parse(sessionStorage.getItem('viewed_ids')),
    viewed: '',
    user_reviews: '',
  },
  modules: {},
  actions: {
    CHECK_USER({commit}) {
      return new Promise((resolve) => {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const anonymous = sessionStorage.getItem('anonymous');
        this._vm.$debug_log(`Token: ${token}`);
        this._vm.$debug_log(`Anonymous: ${anonymous}`);

        if (token) {
          this._vm.$debug_log('Авторизирован');
          store.dispatch('GET_CHECK_TOKEN', token)
            .then(() => {
              resolve();
            });
        } else if (anonymous) {
          resolve();
          //  НЕ ТРОЖ, БУДЕТ ЦИКЛ ВСЕХ ЦИКЛОВ, ВЗЛЕТИШЬ К Е МАТЕРИ
        } else {
          store.dispatch('LOGOUT').then(() => {
            store.dispatch('GET_ANONYMOUS_USER')
              .then(() => {
                resolve();
              });
          });
        }
      });
    },
    GET_ANONYMOUS_USER({commit}) {
      return axios(`${store.state.backendUrlApi}/anonymous/`,
        {
          method: 'POST',
        })
        .then((resp) => {
          commit('SET_ANONYMOUS_TO_STATE', resp.data);
          store.dispatch('GET_CART_DETAIL');
          store.dispatch('GET_COMPARE_DETAIL');
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log(error.response);
          return error;
        });
    },
    GET_CHECK_TOKEN({commit}, token) {
      axios(`${store.getters.getServerUrlApi}/auth/check/`,
        {
          method: 'POST',
          headers: {Authorization: `${store.getters.TOKEN_TYPE} ${token}`},
        })
        .then((resp) => {
          this._vm.$debug_log('Токен подтвержден');
          commit('SET_TOKEN_STATE', token);
          commit('auth_success', token);
          return resp;
        })
        .catch((error) => {
          this._vm.$debug_log(error);
          this._vm.$debug_log('LOGOUT');
          store.dispatch('LOGOUT');
          return error;
        });
    },
    GET_CUSTOMER_DETAIL({commit}, token) {
      if (token) {
        return new Promise((resolve, reject) => {
          axios.defaults.headers.common.Authorization = `${store.getters.TOKEN_TYPE} ${token}`;
          return axios(`${store.state.backendUrlApi}/customer/detail/`,
            window._.merge({
                method: 'POST',
                data: {},
              },
              store.getters.USER_DATA_REQUEST))

            .then((resp) => {
              commit('SET_NULL_TO_ANONYMOUS');
              commit('SET_USER_TO_STORAGE', resp.data);
              commit('auth_success', token);
              store.dispatch('GET_CART_DETAIL');
              store.dispatch('GET_COMPARE_DETAIL');
              resolve(resp);
            })
            .catch((error) => {
              this._vm.$debug_log(error);
              this._vm.$debug_log(error.response);
              store.dispatch('LOGOUT');
              delete axios.defaults.headers.common.Authorization;
              reject(error);
            });
        });
      }
    },
    LOGIN({commit}, data) {
      return new Promise((resolve, reject) => {
        commit('auth_request');
        const {remember} = data;
        axios({
          url: `${store.state.backendUrlApi}/auth/token/login/`,
          data,
          method: 'POST',
        })
          .then((resp) => {
            const token = resp.data.auth_token;
            if (remember) {
              localStorage.setItem('token', token);
            } else {
              sessionStorage.setItem('token', token);
            }
            commit('SET_TOKEN_TYPE', 'Token');
            store.dispatch('GET_CUSTOMER_DETAIL', token)
              .then((response) => {
                resolve(response);
              })
              .catch((error) => {
                reject(error);
              });
          })
          .catch((err) => {
            this._vm.$debug_log(err);
            this._vm.$debug_log(err.response);
            commit('auth_error');
            store.dispatch('LOGOUT');
            reject(err.response);
          });
      });
    },
    REGISTER({commit}, user) {
      this._vm.$debug_log('REGISTER');
      return new Promise((resolve, reject) => {
        commit('auth_request');
        axios({url: `${store.state.backendUrlApi}/auth/users/`, data: user, method: 'POST'})
          .then((resp) => {

            resolve(resp);
          })
          .catch((err) => {
            this._vm.$debug_log(err);
            this._vm.$debug_log(err.response);
            commit('auth_error', err);
            localStorage.removeItem('token');
            sessionStorage.removeItem('token');

            localStorage.removeItem('user');
            sessionStorage.removeItem('user');

            reject(err);
          });
      });
    },
    LOGOUT({commit}) {
      this._vm.$debug_log('LOGOUT');
      if (!axios.defaults.headers.common.Authorization) return
      return new Promise((resolve, reject) => {
        axios(`${store.getters.getServerUrlApi}/auth/token/logout/`,
          window._.merge({
              method: 'POST',
              data: {},
            },
            store.getters.USER_DATA_REQUEST))
          .then((response) => {
            commit('LOGOUT_STATE', response);
            resolve();
          })
          .catch((error) => {
            this._vm.$debug_log(error.response);
            commit('LOGOUT_STATE', error);
            reject();
          });
      });
    },

    GET_USER_REVIEWS({commit}) {
      return new Promise((resolve, reject) => axios(`${store.state.backendUrlApi}/review/customer/`,
        window._.merge({
            method: 'POST',
            data: {},
          },
          store.getters.USER_DATA_REQUEST))
        .then((resp) => {
          commit('SET_USER_REVIEWS_TO_STATE', resp.data);
          resolve(resp);
        })
        .catch((err) => {
          this._vm.$debug_log(err);
          this._vm.$debug_log(err.response);

          reject(err);
        }));
    },

    SEND_EMAIL_TO_RESET_PASSWORD({commit}, data) {
      return new Promise((resolve, reject) => {
        axios({
          url: `${store.state.backendUrlApi}/auth/users/reset_password/`,
          data,
          method: 'POST',
        })
          .then((resp) => {
            resolve(resp);
          })
          .catch((err) => {
            this._vm.$debug_log(err);
            this._vm.$debug_log(err.response);
            reject(err.response);
          });
      });
    },
    CHANGE_PASSWORD({commit}, data) {
      return new Promise((resolve, reject) => {
        axios({
          url: `${store.state.backendUrlApi}/auth/users/reset_password_confirm/`,
          data,
          method: 'POST',
        })
          .then((resp) => {
            resolve(resp);
          })
          .catch((err) => {
            this._vm.$debug_log(err);
            this._vm.$debug_log(err.response);
            reject(err.response);
          });
      });
    },

    SET_CUSTOMER_CHANGES({commit}, data) {
      return new Promise((resolve, reject) => {
        axios(
          window._.merge(
            {
              url: `${store.state.backendUrlApi}/customer/change/`,
              data,
              method: 'POST',
            },
            store.getters.USER_DATA_REQUEST,
          )
        )
          .then((resp) => {
            store.dispatch('GET_CUSTOMER_DETAIL', store.getters.TOKEN).then(() => {
              resolve(resp);
            });
          })
          .catch((err) => {
            this._vm.$debug_log(err);
            this._vm.$debug_log(err.response);
            reject(err.response);
          });
      });
    },

    ADD_VIEWED_PRODUCTS({commit}, data) {
      const viewed = JSON.parse(sessionStorage.getItem('viewed_ids')) || [];
      if (viewed.indexOf(data) === -1) {
        viewed.push(data);
        commit('SET_VIEWED_IDS_TO_STATE', viewed);
      }
    },

    SOCIAL_AUTH({commit}, data) {
      return new Promise((resolve, reject) => {
        axios({
          url: `${store.state.backendUrlApi}/auth/social/token/`,
          data: {
            code: data.code,
            provider: data.provider,
            response: data.response,
            grant_type: 'authorization_code',
            client_id: this._vm.$socialData[data.provider].client_id,
            client_secret: this._vm.$socialData[data.provider].client_secret,
            redirect_uri: this._vm.$socialData[data.provider].redirect_uri,
          },
          method: 'POST',
        })
          .then((resp) => {
            store.dispatch('SOCIAL_AUTH_CONVERT_TOKEN', resp.data);
          })
          .catch((err) => {
            this._vm.$debug_log(err);
            this._vm.$debug_log(err.response);
            reject(err.response);
          });
      });
    },

    SOCIAL_AUTH_CONVERT_TOKEN({commit}, data) {
      return new Promise((resolve, reject) => {
        axios({
          url: `${store.state.backendUrlApi}/auth/social/convert-token`,
          data: {
            token: data.access_token,
            grant_type: 'convert_token',
            backend: `${data.provider.provider}-oauth2`,
            client_id: data.provider.client_id,
            client_secret: data.provider.client_secret,
            redirect_uri: data.provider.redirect_uri,
          },
          method: 'POST',
        })
          .then((resp) => {
            commit('SET_TOKEN_STATE', resp.data.access_token);
            commit('SET_TOKEN_TYPE', resp.data.token_type);

            store.dispatch('GET_CUSTOMER_DETAIL', store.getters.TOKEN);
          })
          .catch((err) => {
            this._vm.$debug_log(err);
            this._vm.$debug_log(err.response);
            reject(err.response);
          });
      });
    },

  },
  getters: {
    IS_LOGGED_IN: (state) => !!state.token,
    authStatus: (state) => state.status,
    TOKEN: (state) => state.token,
    TOKEN_TYPE: (state) => state.token_type,
    FULL_USER_NAME: (state) => {
      if (state.user !== null) {
        if (state.user.first_name && state.user.last_name) {
          return `${state.user.first_name} ${state.user.last_name}`;
        }
      }

      return 'Пользователь';
    },
    USER: (state) => state.user,
    ANONYMOUS: (state) => state.anonymous,

    USER_DATA_REQUEST: () => {
      if (store.getters.TOKEN) {
        axios.defaults.headers.common.Authorization = `${store.getters.TOKEN_TYPE} ${store.getters.TOKEN}`;
        return {
          headers: {
            // 'Accept-Version': 1,
            // 'Accept': 'application/json',
            // 'Accept': "application/json, text/plain, */*",
            // 'Access-Control-Allow-Origin': '*',
            // "Access-Control-Allow-Origin" : "*",
            // "Content-type": "Application/json",
            Authorization: `${store.getters.TOKEN_TYPE} ${store.getters.TOKEN}`,
          },
        };
      }
      if (store.getters.ANONYMOUS) {
        return {
          data: {anonymous: store.getters.ANONYMOUS},
        };
      }
    },

    VIEWED_IDS: (state) => state.viewed_ids,
    VIEWED: (state) => state.viewed,
    USER_REVIEWS: (state) => state.user_reviews,
  },
  mutations: {
    SET_NULL_TO_ANONYMOUS: (state) => {
      Vue.set(state, 'anonymous', null);
      sessionStorage.removeItem('anonymous');
    },
    SET_ANONYMOUS_TO_STATE: (state, anonymous) => {
      Vue.set(state, 'anonymous', anonymous.id);
      sessionStorage.setItem('anonymous', anonymous.id);
    },
    SET_TOKEN_STATE: (state, token) => {
      Vue.set(state, 'token', token);
      localStorage.setItem('token', token);
    },
    SET_TOKEN_TYPE: (state, type) => {
      Vue.set(state, 'token_type', type);
      localStorage.setItem('token_type', type);
    },
    SET_USER_TO_STORAGE: (state, user) => {
      sessionStorage.setItem('user', JSON.stringify(user));
      Vue.set(state, 'user', JSON.parse(sessionStorage.getItem('user')));
    },
    auth_request: (state) => {
      Vue.set(state, 'status', 'loading');
    },
    auth_success: (state, token) => {
      axios.defaults.headers.common.Authorization = `${store.getters.TOKEN_TYPE} ${token}`;
      Vue.set(state, 'status', 'success');
      Vue.set(state, 'token', token);
    },
    auth_error: (state) => {
      Vue.set(state, 'status', 'error');
    },
    LOGOUT_STATE: (state, response) => {
      Vue.set(state, 'status', null);
      Vue.set(state, 'token', null);

      localStorage.removeItem('token');
      sessionStorage.removeItem('token');
      delete axios.defaults.headers.common.Authorization;

      Vue.set(state, 'user', null);
      localStorage.removeItem('user');
      sessionStorage.removeItem('user');

      store.dispatch('GET_ANONYMOUS_USER');
      store.dispatch('START');
    },

    SET_VIEWED_IDS_TO_STATE: (state, data) => {
      data = JSON.stringify(data)
      sessionStorage.setItem('viewed_ids', data);
      Vue.set(state, 'viewed_ids', data);
    },
    SET_VIEWED_TO_STATE: (state, data) => {
      Vue.set(state, 'viewed', data);
    },

    SET_USER_REVIEWS_TO_STATE: (state, data) => {
      Vue.set(state, 'user_reviews', data);
    },
  },
};
