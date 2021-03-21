import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import Vuex, {mapActions} from 'vuex';
// jQuery
import jQuery from 'jquery';
// Валидация форм
import Vuelidate from 'vuelidate';
import 'popper.js';
// axios
import axios from 'axios';
import VueAxios from 'vue-axios';
// LazyLoad IMG
import VueLazyLoad from 'vue-lazyload';
// FA-iconso
import {library} from '@fortawesome/fontawesome-svg-core';
import {
  faGoogle, faInstagram, faTelegram, faYoutube
} from '@fortawesome/free-brands-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
// Bootstrap
import 'bootstrap';
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue';
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
// Дополнительные функции (глубокое слиянение объектов)
import VueLodash from 'vue-lodash';
import lodash from 'lodash';
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
import PhoneNumber from 'awesome-phonenumber';
//VueSkeletonLoading
//https://github.com/jiingwang/vue-skeleton-loading
import VueSkeletonLoading from 'vue-skeleton-loading';
//
import router from './router';
import service from './service';
import store from './store';
//Vue WebSocket
import VueNativeSock from 'vue-native-websocket'

Vue.use(VueNativeSock, 'ws://localhost:8000/ws/notifications/', {
  store: store,
  format: 'json',
  reconnection: true,
  reconnectionAttempts: 10,
  reconnectionDelay: 5000,
})

//Switchers
import ToggleButton from 'vue-js-toggle-button'
import {faCopy} from "@fortawesome/free-solid-svg-icons";

Vue.use(ToggleButton)


Vue.use(VueClipboard);
Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);

Vue.use(Vuex);

Vue.use(VueSkeletonLoading);

window.$ = window.jQuery = jQuery;

Vue.use(Vuelidate);

Vue.use(VueAxios, axios);
Vue.prototype.$axios = axios;

Vue.use(VueLazyLoad);

Vue.component('font-awesome-icon', FontAwesomeIcon);
library.add(faInstagram, faYoutube, faTelegram, faGoogle, faCopy);
Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(LoadScript);
Vue.component('paginate', Paginate);
Vue.use(PrettyCheckbox);
Vue.use(VueLodash, {name: 'custom', lodash});
Vue.use(Toasted);
Vue.use(VueSocialauth, {
  providers: {
    google: {
      clientId: '1072563183925-8t7ri7d7ikbjcrfna2bu123pt93t90su.apps.googleusercontent.com',
      redirectUri: 'http://localhost:8080', // Your client app URL
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
    ...mapActions(['START']),
  },

  mounted() {
    this.START();
  },
  render: (h) => h(App)
}).$mount('#app');

// http://localhost:8080/?code=4%2F0AY0e-g4QywM-gFjVs3kpTH56mFoHlMpIg7Wo2CYepaPZw__wGHq8RSQOd06vGeX23V1HOA&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+openid&authuser=0&prompt=none

//
//
//
//
//
//
//
//
//
//
//
//

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
      const phone = new PhoneNumber(value);
      resolve({valid: phone.isValid()});
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
