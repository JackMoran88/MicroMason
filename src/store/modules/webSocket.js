import Vue from 'vue';
import Vuex from 'vuex';
import store from '../index';
import router from '@/router';

Vue.use(Vuex);


export default ({
  state: {
    socket: {
      isConnected: false,
      message: '',
      reconnectError: false,
    }
  },
  mutations: {
    SOCKET_ONOPEN(state, event) {
      console.log(':::WebSocket:::')
      Vue.prototype.$socket = event.currentTarget
      state.socket.isConnected = true
    },
    SOCKET_ONCLOSE(state, event) {
      state.socket.isConnected = false
    },
    SOCKET_ONERROR(state, event) {
      console.error(state, event)
    },
    SOCKET_ONMESSAGE(state, message) {
      store.dispatch('SOCKET_CATCH', message)
      state.socket.message = message
    },
    SOCKET_RECONNECT(state, count) {
      console.info(state, count)
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    },
  },
  actions: {
    SOCKET_SEND_MESSAGES(context, message) {
      let data = {
        data: message
      }
      data = JSON.stringify(data)
      Vue.prototype.$socket.send(data)
      console.log('::WebSocket::')
    },
    SOCKET_CATCH(context, message) {
      let route = router.history.current
      switch (message.type) {
        case 'UPDATE_PRODUCT':
          let curProduct = parseInt(store.getters.PRODUCT.id)
          let updProduct = parseInt(message.payload)
          if(curProduct !== updProduct) return

          store.dispatch('GET_PRODUCT_BY_ID', store.getters.PRODUCT.id).then((product) => {
            this._vm.$toast('attention', 'Продукт получил обновление')
            router.replace(
              {
                query: Object.assign({}, route.query),
                params: {
                  ProductSlug: product.slug,
                  slug: product.category_slug
                }
              }
            ).catch(() => {
            })
          })
          break
        default:
          break
      }
    },

  }
})
