<template>
  <div class="page">
    <v-header/>
    <div class="page__wrapper container">
      <transition name="fade" mode="out-in">
        <router-view/>
      </transition>
      <v-drop-catalog/>
    </div>
    <v-footer/>

      <v-modals/>

    <v-loading/>
    <v-back-to-top/>
  </div>
</template>

<script>
import vHeader from '@/components/app/v-header.vue';
import vFooter from '@/components/app/v-footer.vue';
import vMobileMenu from '@/components/app/mobile/slideMenu.vue';
import vModals from '@/components/modal/v-modals.vue';
import vLoading from '@/components/app/func/v-loading.vue';
import vDropCatalog from '@/components/app/catalog/v-drop-catalog.vue';

import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'MainLayout',
  components: {
    vHeader, vFooter, vMobileMenu, vModals, vDropCatalog, vLoading,
  },
  data: () => ({}),
  methods: {
    json() {
      return {
        public_key: 'i00000000',
        version: '3',
        action: 'pay',
        amount: '3',
        currency: 'UAH',
        description: 'test',
        order_id: '000001',
      };
    },

    ...mapActions(['GET_CATEGORY_LIST', 'GET_SOCKET']),
  },
  computed: {
    ...mapGetters(['CATEGORIES', 'SETTINGS', 'SOCKET']),
  },
  mounted() {
    // this.GET_SOCKET();
  },
};
</script>

<style lang="scss">
  div.page {
    background: var(--background-content);
    width: 100%;

    .page__wrapper {
      display: flex;
      position: relative;
      margin: 0 !important;
      min-height: 90vh;
      padding-top: .5rem;

      section.left {
        background: blue;
      }

      section.center {
        padding: 0;
      }

      section.right {
        background: green;
      }
    }
  }

  a, a:hover {
    text-decoration: none;
    cursor: pointer;
  }

  .backdrop {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    z-index: 30;
    background: rgba(black, .5);
  }

</style>

<style lang="scss">
  $toast-bg__success: rgb(33, 152, 104);
  $toast-bg__info: rgb(22, 106, 170);
  $toast-bg__error: rgb(185, 42, 7);
  $toast-bg__attention: rgb(183, 129, 1);
  $toast-bg__test: rgb(44, 47, 49);

  .toasted-container {
    &.top-right {
      right: 1% !important;
      max-width: 350px;
    }

    .toasted {
      &.toast {
        padding: 1rem 1.25rem;
        border-radius: .5rem !important;

        i {
          margin-right: 1rem;
          @include fz(24);
        }

        &__success {
          color: white;
          background: $toast-bg__success;
        }

        &__info {
          color: white;
          background: $toast-bg__info;
        }

        &__error {
          color: white;
          background: $toast-bg__error;
        }

        &__attention {
          color: white;
          background: $toast-bg__attention;
        }

        &__test {
          color: white;
          background: $toast-bg__test;
        }
      }
    }

  }

</style>
