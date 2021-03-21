// import router from '@/router';
// import store from '../index';
//
// export default {
//   state: {
//     socket: new WebSocket(
//       'ws://'
//       + 'localhost:8000'
//       + '/ws/notifications'
//       + '/',
//     ),
//   },
//   modules: {},
//   actions: {
//     GET_SOCKET() {
//       const Socket = this.getters.SOCKET;
//
//       Socket.onopen = function () {
//         console.log('WebSocket: подключен');
//       };
//
//       Socket.onerror = function (e) {
//         console.log('WebSocket error');
//         console.log(e);
//       };
//
//       Socket.onclose = function () {
//         console.error('WebSocket close');
//       };
//     },
//     GET_SOCKET_CHANNEL(e, channel) {
//       const Socket = this.getters.SOCKET;
//       // Socket.onopen = function (channel) {
//       Socket.send(JSON.stringify({
//         data: channel,
//       }));
//       // };
//       console.log(`WebSocket: канал(ы) ( ${channel} ) подключен(ы)`);
//     },
//     SOCKET_CATCH(e, userData) {
//       const vue = this._vm;
//       const Socket = this.getters.SOCKET;
//       Socket.onmessage = function () {
//         console.log('WebSocket: пришло обновление');
//         const data = JSON.parse(e.data);
//         if (data.type === 'UPDATE_PRODUCT') {
//           if (userData.ProductId === data.payload) {
//             store.dispatch('GET_PRODUCT_BY_ID', userData.ProductId).then((product) => {
//               router.replace({
//                 path: router.history.current.path,
//                 params: {
//                   slug: product.category_slug,
//                   ProductSlug: product.slug,
//                 },
//               })
//                 .catch(() => {
//                   vue.$debug_log('reRoute error');
//                 });
//             });
//           }
//         }
//       };
//     },
//   },
//   getters: {
//     SOCKET: (state) => state.socket,
//   },
//   mutations: {
//     SET_SOCKET_TO_STATE: (state, socket) => {
//       state.socket = socket;
//     },
//   },
// };
