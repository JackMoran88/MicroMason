<template>
  <div class="page">

    {{$store.state.user_drop_data}}
    <v-header/>

    <div class="page__wrapper container">
      <transition name="fade" mode="out-in">
        <router-view/>
      </transition>
      <v-drop-catalog
        v-if="IS_DESKTOP"
      />
    </div>

    <v-footer/>
    <v-modals/>

    <!--    <v-loading/>-->

    <v-back-to-top/>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex';
  import vHeader from '@/components/app/v-header.vue';
  import vFooter from '@/components/app/v-footer.vue';
  import vMobileMenu from '@/components/app/mobile/slideMenu.vue';
  import vModals from '@/components/modal/v-modals.vue';
  import vLoading from '@/components/app/func/v-loading.vue';
  import vDropCatalog from '@/components/app/catalog/v-drop-catalog.vue';
  import store from "../store";

  export default {
    name: 'MainLayout',
    components: {
      vHeader, vFooter, vMobileMenu, vModals, vDropCatalog, vLoading,
      // vHeader: () => import('@/components/app/v-header.vue'),
      // vFooter: () => import('@/components/app/v-footer.vue'),
      // vMobileMenu: () => import('@/components/app/mobile/slideMenu.vue'),
      // vModals: () => import('@/components/modal/v-modals.vue'),
      // vLoading: () => import('@/components/app/func/v-loading.vue'),
      // vDropCatalog: () => import('@/components/app/catalog/v-drop-catalog.vue'),
    },
    data: () => ({}),
    methods: {},
    computed: {
      ...mapGetters(['IS_DESKTOP']),
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


</style>
