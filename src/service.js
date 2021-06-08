import store from './store';
import router from '@/router';
import axios from "axios";

export default {

  install(Vue, options) {
    Vue.prototype.$socialData = {
      google: {
        client_id: '1072563183925-8t7ri7d7ikbjcrfna2bu123pt93t90su.apps.googleusercontent.com',
        client_secret: 'IWH3HU3Lpvcp25_PHXeuhL6q',
        redirect_uri: process.env.VUE_APP_BACKEND_URL,
      },
    };

    Vue.prototype.$scrollToTop = function (duration = 500) {
      // cancel if already on top
      if (document.scrollingElement.scrollTop === 0) return;

      const totalScrollDistance = document.scrollingElement.scrollTop;
      let scrollY = totalScrollDistance;
      let
        oldTimestamp = null;

      function step(newTimestamp) {
        if (oldTimestamp !== null) {
          // if duration is 0 scrollY will be -Infinity
          scrollY -= totalScrollDistance * (newTimestamp - oldTimestamp) / duration;
          if (scrollY <= 0) return document.scrollingElement.scrollTop = 0;
          document.scrollingElement.scrollTop = scrollY;
        }
        oldTimestamp = newTimestamp;
        window.requestAnimationFrame(step);
      }

      window.requestAnimationFrame(step);
    };
    Vue.prototype.$productStatus = function (status) {
      if (['1', '3'].includes(status)) {
        return true;
      }
      return false;
    };
    Vue.prototype.$debug_log = function (data, msg = '') {
      if (store.getters.DEBUG) {
        if (msg) {
          msg = `${msg.toUpperCase()} :`;
        }
        console.log(msg, data);
      }
    };

    Vue.prototype.$search_by = function (data, parameter, value) {
      return data.filter((obj) => obj[parameter] === value)[0];
    };

    Vue.prototype.$data_not_null = function (data) {
      for (const key in data) {
        if (!data[key]) {
          return false;
        }
      }
      return true;
    };

    Vue.prototype.$serialize_query = function (data) {
      let str = '';
      for (const key in data) {
        if (str !== '') {
          str += '&';
        }
        str += `${key}=${encodeURIComponent(data[key])}`;
      }

      return str ? `?${str}` : str;
    };

    Vue.prototype.$update_query_url = function () {
      //Без этого хлебные крошки будут обновляться не правильно
      this.$router.replace({query: Object.assign({}, this.$route.query, {temp: Date.now()})})
      this.$router.replace({query: Object.assign({}, this.$route.query, {temp: undefined})})
    }

    Vue.prototype.$change_query_url = function (data) {
      this.$router.replace({query: Object.assign({}, this.$route.query, data)}).catch(() => {
      })
    }

    Vue.prototype.$clear_query_url = function (data) {
      delete this.$route.query[data]
      this.$update_query_url()
    }

    Vue.prototype.$submitFilters = function () {
      let data = {
        slug: this.$route.params.slug,
        filters: this.$serialize_query(this.$route.query)
      }
      this.$store.dispatch('GET_PRODUCTS', data)
    }

    Vue.prototype.$request_errors = function (request) {
      let result = [];
      let errors = [];
      if ('response' in request) {
        errors = request.response.data;
      } else if ('data' in request) {
        errors = request.data;
      }
      result = Object.values(errors);
      // НЕКОТОРЫЕ ОШИБКИ В МАСИВЕ МАСИВОВ
      result.forEach((value, index) => {
        if (Array.isArray(value)) {
          result[index] = value[0];
        }
      });

      return result;
    };

    Vue.prototype.$USER_DATA_REQUEST = function () {
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
          params: {anonymous: store.getters.ANONYMOUS},
        };
      }
    },

    Vue.prototype.$toast = function (type, message = 'Text', duration = 5000, position = 2) {
      switch (position) {
        case 0:
          position = 'top-left';
          break;
        case 1:
          position = 'top-right';
          break;
        case 2:
          position = 'bottom-right';
          break;
        case 3:
          position = 'bottom-left';
          break;
      }
      switch (type) {
        case 'success':
          this.$toasted.show(message, {
            icon: 'check_circle',
            position,
            duration,
            className: 'toast toast__success',
          });
          break;
        case 'error':
          this.$toasted.show(message, {
            icon: 'cancel',
            position,
            duration,
            className: 'toast toast__error',
          });
          break;
        case 'attention':
          this.$toasted.show(message, {
            icon: 'warning',
            position,
            duration,
            className: 'toast toast__attention',
          });
          break;
        case 'info':
          this.$toasted.show(message, {
            icon: 'info',
            position,
            duration,
            className: 'toast toast__info',
          });
      }
    };
  },
};
