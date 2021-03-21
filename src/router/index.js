import Vue from 'vue';
import VueRouter from 'vue-router';
import Meta from 'vue-meta';
import Index from '@/views/Index.vue';
import Empty from '@/views/Empty.vue';
import Category from '@/views/Category.vue';
import Search from '@/views/Search.vue';
import Categories from '@/views/Categories.vue';
import NotFound from '@/views/NotFound.vue';
import ServerProblem from '@/views/ServerProblem.vue';
import Checkout from '@/views/Checkout.vue';
import Product from '../views/Product.vue';
import store from '../store/index.js';
import Comparison from '../views/Comparison';

Vue.use(VueRouter);
Vue.use(Meta);

Comparison;

const routes = [
  {
    name: 'NotFound',
    path: '/404',
    component: NotFound,
  }, {
    path: '*',
    redirect: '404',
  },

  {
    name: 'ServerProblem',
    path: '/503',
    component: ServerProblem,
    meta: {
      layout: 'Empty',
    },
  },

  {
    name: 'SocialAuth',
    path: '/auth/:provider/callback/',
    meta: {
      layout: 'Empty',
    },
  },

  {
    path: '/',
    name: 'Home',
    component: Index,
    meta: {
      layout: 'main',
      breadcrumb: {
        label: 'Главная',
      },
    },
  },
  {
    path: '/category/:slug/',
    component: Category,
    name: 'Category',
    meta: {
      layout: 'main',
      breadcrumb: {
        label: 'Категория',
        parent: 'Home',
      },
    },
    props: true,
  },

  {
    path: '/category/:slug/product/:ProductSlug/',
    name: 'Product',
    meta: {
      layout: 'main',
      breadcrumb: {
        tab: 'tab-main',
        label: 'Товар',
        parent: 'Category',
      },
    },
    props: true,
    component: Product,
    children: [
      {
        path: '/category/:slug/product/:ProductSlug/comments',
        name: 'Product review',
        meta: {
          layout: 'main',
          tab: 'tab-review',
          breadcrumb: 'Коментарии',
        },
        props: true,
        component: Product,
      },
      {
        path: 'characteristics',
        name: 'Product characteristics',
        meta: {
          layout: 'main',
          tab: 'tab-spec',
          breadcrumb: 'Характеристики',
        },
        props: true,
        component: Product,
      },
    ],
  },

  {
    path: '/checkout',
    name: 'Checkout',
    meta: {
      layout: 'main',
      breadcrumb: {
        label: 'Оформление заказа',
        parent: 'Home',
      },
    },
    props: true,
    component: Checkout,
  },

  {
    path: '/search',
    component: Search,
    name: 'Search',
    meta: {
      layout: 'main',
      breadcrumb: {
        label: 'Поиск',
        parent: 'Home',
      },
    },
    props: true,
  },

  {
    path: '/account',
    name: 'Account',
    meta: {
      layout: 'main',
      breadcrumb: {
        label: 'Аккаунт',
        // parent: 'Home'
      },
      // requiresAuth: true, //Если не авторизирован

    },
    component: () => import('@/views/Account/Account.vue'),
    children: [
      {
        path: '',
        name: 'Account main',
        meta: {
          layout: 'main',
          breadcrumb: 'Личные данные',
          requiresAuth: true, // Если не авторизирован

        },
        component: () => import('@/views/Account/Main.vue'),
      },
      {
        path: 'wish',
        name: 'Account wish',
        meta: {
          layout: 'main',
          breadcrumb: 'Избранное',
          requiresAuth: false,

        },
        component: () => import('@/views/Account/Wish.vue'),
      },
      {
        path: 'comparison',
        component: Comparison,
        name: 'Account comparison',
        meta: {
          layout: 'main',
          breadcrumb: 'Сравнение',
          requiresAuth: false,
        },
        props: true,
      },
      {
        path: 'reviews',
        name: 'Account reviews',
        meta: {
          layout: 'main',
          breadcrumb: 'Отзывы',
          requiresAuth: true, // Если не авторизирован

        },
        component: () => import('@/views/Account/Reviews.vue'),
      },
      {
        path: 'orders',
        name: 'Account orders',
        meta: {
          layout: 'main',
          breadcrumb: 'Заказы',
          requiresAuth: true, // Если не авторизирован

        },
        component: () => import('@/views/Account/Orders.vue'),
      },
    ],
  },

  {
    path: '/user',
    name: 'User',
    meta: {
      layout: 'main',
      requiresAuth: false,

    },
    component: () => import('@/views/Account/User.vue'),
    children: [
      {
        path: 'password/reset/confirm/:uid/:token',
        name: 'User password reset',
        meta: {
          layout: 'main',
          requiresAuth: false,
        },
        component: () => import('@/views/Account/User.vue'),
      },
    ],
  },

];

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes,
  mode: 'history',
});

// Для предотвращения ошибки о дубликате url
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err);
};

// Если пользователь перешел на несуществующую страницу
router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (store.getters.IS_LOGGED_IN) {
      next();
      return;
    }
    next('/');
  } else {
    next();
  }
});

export default router;
