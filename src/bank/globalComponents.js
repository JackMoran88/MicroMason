import Vue from 'vue';

import vBtn from '@/components/app/button/v-btn.vue';

import vHeaderCart from '@/components/app/button/v-header-cart.vue';
import vHeaderWish from '@/components/app/button/v-header-wish.vue';
import vHeaderComapre from '@/components/app/button/v-header-compare.vue';
import vHeaderSearch from '@/components/app/form/v-header-search.vue';
import vBackToTop from '@/components/app/v-back-to-top.vue';

import vLiqPay from '@/components/order/v-liq-pay.vue';

// import read_more from '@/components/app/func/v-read-more'

import quantity from '@/components/product/v-quantity.vue';
import vPaginate from '@/components/app/v-paginate.vue';
import vLoadingAnimation from '@/components/app/func/v-loading-animation.vue';
import vCurrency from '@/components/app/v-currency.vue';
// import vSelect from '@/components/app/form/v-select.vue';
import vSortBy from '@/components/app/v-sort-by.vue';
import vAttention from '@/components/app/headers/v-attention.vue';
import vTitle from '@/components/app/headers/v-title.vue';
import vTitleSmall from '@/components/app/headers/v-title-small.vue';

import vInput from '@/components/app/form/v-input.vue';
import vForm from '@/components/app/form/v-form.vue';

import vViewedProducts from '@/components/app/container/v-viewed-products.vue';
import vCustomProductsLine from '@/components/app/container/v-custom-products-line.vue';
import vGrid from '@/components/app/container/v-grid.vue';
import vItemsContainer from '@/components/app/container/v-items-container.vue';
import vQuickCopy from '@/components/app/container/v-quick-copy.vue';
import vFilterBoard from '@/components/app/container/v-filter-board.vue';

import vSlider from '@/components/app/container/v-slider.vue';

import StarRating from 'vue-star-rating';

import ReadMore from 'vue-read-more';

Vue.component('vBtn', vBtn);
// Vue.component('v-read-more', read_more)
Vue.component('header-cart', vHeaderCart);
Vue.component('header-wish', vHeaderWish);
Vue.component('header-compare', vHeaderComapre);
Vue.component('header-search', vHeaderSearch);
Vue.component('quantity', quantity);
Vue.component('loading-animation', vLoadingAnimation);
Vue.component('vCurrency', vCurrency);
// Vue.component('vSelect', vSelect);
Vue.component('vPaginate', vPaginate);
Vue.component('vSortBy', vSortBy);
Vue.component('vAttention', vAttention);
Vue.component('vTitle', vTitle);
Vue.component('vTitleSmall', vTitleSmall);

Vue.component('vViewedProducts', vViewedProducts);
Vue.component('vCustomProductsLine', vCustomProductsLine);
Vue.component('vGrid', vGrid);
Vue.component('vItemsContainer', vItemsContainer);
Vue.component('vQuickCopy', vQuickCopy);
Vue.component('vFilterBoard', vFilterBoard);

Vue.component('vInput', vInput);
Vue.component('vForm', vForm);

Vue.component('vSlider', vSlider);
Vue.component('vBackToTop', vBackToTop);

Vue.component('vLiqPay', vLiqPay);

Vue.component('star-rating', StarRating);

Vue.use(ReadMore);

Vue.directive('click-outside', {
  bind(el, binding, vnode) {
    el.clickOutsideEvent = function (event) {
      // here I check that click was outside the el and his children
      if (!(el === event.target || el.contains(event.target))) {
        // and if it did, call method provided in attribute value
        vnode.context[binding.expression](event);
      }
    };
    document.body.addEventListener('click', el.clickOutsideEvent);
  },
  unbind(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent);
  },
});
