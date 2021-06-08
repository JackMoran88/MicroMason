import Vue from 'vue';
import App from './App.vue';
import router from './router';
import service from './service';
import store from './store';
import './registerServiceWorker';
import Vuex from 'vuex';
// axios
import axios from 'axios';
import VueAxios from 'vue-axios';
// LazyLoad IMG
import VueLazyLoad from 'vue-lazyload';
// Bootstrap
import 'popper.js';
import { CarouselPlugin, ModalPlugin, VBTogglePlugin, SidebarPlugin} from 'bootstrap-vue'
Vue.use(CarouselPlugin)
Vue.use(ModalPlugin)
Vue.use(VBTogglePlugin)
Vue.use(SidebarPlugin)

import 'bootstrap-vue/dist/bootstrap-vue.css';
// BreadCrumbs
import VueBreadcrumbs from 'vue-2-breadcrumbs';
import {dragscroll} from 'vue-dragscroll';
// Загрузка внешник скриптов
import LoadScript from 'vue-plugin-load-script';
// Paginate
import Paginate from 'vuejs-paginate';
// Импорт глобальных компонентов
import '@/bank/globalComponents';
// Checkbox
import PrettyCheckbox from 'pretty-checkbox-vue';
// Глубокое слиянение объектов
import VueLodash from 'vue-lodash';
import merge from 'lodash/merge'
// Toast
import Toasted from 'vue-toasted';
// Social oAuth
import VueSocialauth from 'vue-social-auth';
// Quick Clipboard
import VueClipboard from 'vue-clipboard2';
// Vue meta
import VueMeta from 'vue-meta';
// Vue select
import vSelect from 'vue-select'

Vue.component('v-select', vSelect)
import 'vue-select/dist/vue-select.css';
// Vee Validate
import {extend, ValidationObserver, ValidationProvider} from 'vee-validate';
import {
  alpha, confirmed, email, required,
} from 'vee-validate/dist/rules';
// import PhoneNumber from 'awesome-phonenumber';

//VueSkeletonLoading
import VueSkeletonLoading from 'vue-skeleton-loading';
//Vue WebSocket
import VueNativeSock from 'vue-native-websocket'
//Switchers
import ToggleButton from 'vue-js-toggle-button'


Vue.use(VueNativeSock, `ws://${process.env.VUE_APP_BACKEND_IP}/api/ws/notifications/`, {
  store: store,
  format: 'json',
  reconnection: true,
  reconnectionAttempts: 10,
  reconnectionDelay: 5000,
})

import "@/assets/styles/bootstrap.scss";
import "@/assets/styles/styles.scss";
import 'pretty-checkbox/src/pretty-checkbox.scss';

Vue.use(ToggleButton)

Vue.use(VueClipboard);
Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);

Vue.use(Vuex);

Vue.use(VueSkeletonLoading);

Vue.use(VueAxios, axios);
Vue.prototype.$axios = axios;

Vue.use(VueLazyLoad);

Vue.config.productionTip = false;

Vue.use(LoadScript);
Vue.component('paginate', Paginate);
Vue.use(PrettyCheckbox);
Vue.use(VueLodash, {name: 'custom', lodash: {merge}});
Vue.use(Toasted);

Vue.use(VueSocialauth, {
  providers: {
    google: {
      clientId: '1072563183925-8t7ri7d7ikbjcrfna2bu123pt93t90su.apps.googleusercontent.com',
      redirectUri: process.env.VUE_APP_BACKEND_URL, // Your client app URL
      // redirectUri: 'https://oauth2.googleapis.com/token' // Your client app URL
    },
  },
});

Vue.use(VueMeta, {
  // optional pluginOptions
  refreshOnceOnNavigation: true,
});

Vue.use(service);
Vue.use(service, {
  someOption: true,
});


// Breadcrumbs template
Vue.use(VueBreadcrumbs, {
  template:
    '        <nav v-if="$breadcrumbs.length > 1" class="breadcrumb-container" aria-label="breadcrumb">\n'
    + '            <ol class="breadcrumb" v-dragscroll>\n'
    + '                <li v-for="(crumb, index, key) in $breadcrumbs" v-if="crumb.meta.breadcrumb" :key="key" class="breadcrumb-item active" aria-current="page">\n'
    + '                    <router-link v-if="index + 1 <  $breadcrumbs.length" :to="{ path: getPath(crumb) }">{{ getBreadcrumb(crumb.meta.breadcrumb) }}</router-link>'
    + '                       <span v-else>{{ getBreadcrumb(crumb.meta.breadcrumb)}}</span>'
    + '                </li>\n'
    + '            </ol>\n'
    + '        </nav>',
  directives: {
    dragscroll,
  },
});

export const eventBus = new Vue();

new Vue({
  router,
  store,

  methods: {
    // ...mapActions(['START']),
  },

  mounted() {
    store.dispatch('GET_SHOP_SLIDERS');
  },
  render: (h) => h(App)
}).$mount('#app');

extend('required', {
  ...required,
  message() {
    return 'Поле должно быть заполнено';
  },
});
extend('confirmed', {
  ...confirmed,
  message() {
    return 'Поля должны совпадать';
  },
});
extend('email', {
  ...email,
  message() {
    return 'Поле должно содержать Email';
  },
});
extend('alpha', {
  ...alpha,
  message() {
    return 'Поле должно содержать только буквы';
  },
});
extend('minmax', {
  validate(value, args) {
    const {length} = value;

    return length >= args.min && length <= args.max;
  },
  params: ['min', 'max'],
  message(value, args) {
    return `Минимальное к-во символов: ${args.min}, максимальное: ${args.max}`;
  },
});
extend('phone', {
  validate(value) {
    return new Promise((resolve) => {
      let re = /\+380\d{3}\d{2}\d{2}\d{2}$/
      resolve({valid: re.test(value)});
    });
  },
  message(value) {
    return `Номер телефона введен не верно! Пример: +380970000000`;
  },
});
extend('password', {
  validate(value) {
    return new Promise((resolve) => {
      // const re = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
      const re = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
      resolve({valid: re.test(value)});
    });
  },
  message(value) {
    return `Некоректный пароль. Пароль должен состоять из восьми или более символов латинского алфавита, содержать заглавные и строчные буквы, цифры`;
  },
});
