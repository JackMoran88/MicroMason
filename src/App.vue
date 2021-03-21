<template>
  <div id="app">
    <transition name="fade">
      <component :is="layout">
        <router-view/>
      </component>
    </transition>
  </div>
</template>

<script>
  import MainLayout from '@/layouts/MainLayout.vue';
  import EmptyLayout from '@/layouts/EmptyLayout.vue';
  import {mapActions, mapGetters} from 'vuex';

  export default {
    components: {
      MainLayout, EmptyLayout,
    },
    methods: {
      ...mapActions(['SET_MOBILE', 'SET_DESKTOP', 'SOCKET_SEND_MESSAGES', 'SOCKET_CONNECT']),
    },
    computed: {
      layout() {
        return `${this.$route.meta.layout || 'main'}-layout`;
      },
      ...mapGetters(['IS_MOBILE', 'IS_DESKTOP', 'SETTINGS']),
    },
    mounted() {

    },
    watch: {
      $route() {
        this.$scrollToTop();
      },
    },
    metaInfo() {
      let data = {
        title: 'MicroMason',
        meta: [
          {vmid: 'description', property: 'description', content: 'description'},
          {vmid: 'og:description', property: 'og:description', content: 'description'},
          {vmid: 'og:title', property: 'og:title', content: 'title'},
        ],
      };
      if (this.SETTINGS && this.SETTINGS.meta_description) {
        let description = this.SETTINGS.meta_description
        let {title} = this.SETTINGS;
        data = {
          title: 'MicroMason',
          meta: [
            {vmid: 'description', property: 'description', content: description},
            {vmid: 'og:description', property: 'og:description', content: description},
            {vmid: 'og:title', property: 'og:title', content: title},
          ],
        };
      }
      return data
    },
  };
</script>

<style lang="scss">
  /*@import url("https://fonts.googleapis.com/css?family=Material+Icons|Material+Icons+Outlined|Material+Icons+Two+Tone|Material+Icons+Round|Material+Icons+Sharp");*/
  @import "assets/styles/fonts.scss";
  @import "assets/styles/scss.scss";
  @import "assets/styles/bootstrap.scss";
  @import "assets/styles/colors.scss";
  @import "assets/styles/components.scss";
  @import "assets/styles/animations.scss";
  @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;500;600;700&display=swap');
  $pretty--color-primary: #424e65;
  @import '~pretty-checkbox/src/pretty-checkbox.scss';
  html {
    overflow-x: hidden;
  }

  #app {
    min-height: 100%;
    height: 100%;
  }

  body {
    @extend %_font;

    & {
      color: var(--text-main);
    }
  }

  .disabled {
    &, * {
      color: var(--text-second);
    }
  }

  *:focus {
    outline: none !important;
  }

  #readmore {
    @include link
  }

  li {
    a {
      color: inherit;
    }
  }

  @media (max-width: 576px) {
    .container, .container-fluid, .container-sm, .container-md, .container-lg, .container-xl {
      padding-left: 7px;
      padding-right: 7px;
    }
  }

  .table {
    margin: 0;
    color: var(--text-main);

    &-border {
      @include def-border;
    }

    tr {
      td, th {
        border: none;
        text-align: center;

        &:first-of-type {
          text-align: left;
        }

        &:last-of-type {
          text-align: right;
        }
      }
    }
  }

  .btn-reply {
    padding: .375rem 0;
  }

  .btn-close {
    display: flex;
    justify-content: center;
    align-items: center;
    background: none;
    border: none;

    &:focus {
      outline: none !important;
      border: none;
    }
  }

  .btn-search {
    width: 38px;
    height: 100%;
    padding: 0.175rem 0.55rem;

    img {
      max-height: 100%;
      max-width: 100%;
      filter: invert(95%) sepia(4%) saturate(1456%) hue-rotate(188deg) brightness(99%) contrast(81%);
    }
  }

  .card-btn {
    box-sizing: content-box;
    @extend %_material-icons;
    color: var(--card-button);
    height: 35px;
    width: 35px;
    background: var(--background-light);
    background-size: 80% 80% !important;
    background-position: center !important;
    padding: 0;
    border-radius: 50%;
  }

  .btn-wish {
    @include fz(26);
    @extend %_material-icons;
    transition: background-image .25s ease-in-out;

    &:after {
      content: 'favorite_border';
    }

    &.fill {
      color: red;

      &:after {
        content: 'favorite';
      }
    }

    &:hover {
      color: red;
    }

    &:focus {
      box-shadow: none;
    }
  }

  .btn-compare {
    @include fz(26);
    @extend %_material-icons;
    transition: background-image .25s ease-in-out;

    &:after {
      content: 'compare_arrows';
    }

    &.fill {
      color: var(--link-hover);

      &:after {
        content: 'compare_arrows';
        color: var(--link-hover);
      }
    }

    &:hover {
      color: var(--accent);
    }

    &:focus {
      box-shadow: none;
    }
  }

  .btn-quick-view {
    @include fz(26);
    transition: background-image .25s ease-in-out;

    &:after {
      content: 'visibility';
    }

    &.fill {
      color: royalblue;

      &:after {
        content: 'visibility';
        color: royalblue;
      }
    }

    &:hover {
      color: royalblue;
    }

    &:focus {
      box-shadow: none;
    }
  }

  /*PRODUCT*/
  .btn-action {
    box-sizing: content-box;
    height: 14px;
    width: 10px;
    background-size: 80% 80% !important;
    background-position: center !important;
    background: var(--background-light) url("../src/assets/svg/func/vertical-dots-empty.png") no-repeat;
    //background-size: contain;
    background-repeat: no-repeat;
    transition: background-image .25s ease-in-out;

    &.fill, &:hover {
      background-image: url("../src/assets/svg/func/vertical-dots-fill.png");
    }

    &:focus {
      box-shadow: none;
    }
  }

  .btn {
    &.disabled, &:disabled {
      color: var(--text-btn-disabled) !important;
      background-color: var(--border-btn-disabled) !important;
      border-color: var(--background-btn-disabled) !important;
    }
  }

  .btn-primary {
    color: var(--text-btn-primary);
    background-color: var(--background-btn-primary);
    border-color: var(--border-btn-primary);

    &:hover, &:focus, &.focus {
      color: var(--text-btn-primary);
      background-color: var(--border-btn-primary);
      border-color: var(--background-btn-primary);
    }
  }

  .btn-info {
    color: #fff;
    background-color: #17a2b8;
    border-color: #17a2b8;

    &:hover {
      color: #fff;
      background-color: #138496;
      border-color: #117a8b;
    }

    &:focus, &.focus {
      color: #fff;
      background-color: #138496;
      border-color: #117a8b;
      box-shadow: 0 0 0 0.2rem rgba(58, 176, 195, 0.5);
    }

    &.disabled, &:disabled {
      color: #fff;
      background-color: #17a2b8;
      border-color: #17a2b8;
    }
  }

  .btn-warning {
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;

    &:hover {
      color: #212529;
      background-color: #e0a800;
      border-color: #d39e00;
    }

    &:focus, &.focus {
      color: #212529;
      background-color: #e0a800;
      border-color: #d39e00;
      box-shadow: 0 0 0 0.2rem rgba(222, 170, 12, 0.5);
    }

    &.disabled, &:disabled {
      color: #212529;
      background-color: #ffc107;
      border-color: #ffc107;
    }
  }

  .btn-light {
    color: #212529;
    background-color: #f8f9fa;
    border-color: #f8f9fa;

    &:hover {
      color: #212529;
      background-color: #e2e6ea;
      border-color: #dae0e5;
    }

    &:focus, &.focus {
      color: #212529;
      background-color: #e2e6ea;
      border-color: #dae0e5;
      box-shadow: 0 0 0 0.2rem rgba(216, 217, 219, 0.5);
    }

    &.disabled, &:disabled {
      color: #212529;
      background-color: #f8f9fa;
      border-color: #f8f9fa;
    }
  }

  .btn-dark {
    color: #fff;
    background-color: #343a40;
    border-color: #343a40;

    &:hover {
      color: #fff;
      background-color: #23272b;
      border-color: #1d2124;
    }

    &:focus, &.focus {
      color: #fff;
      background-color: #23272b;
      border-color: #1d2124;
      box-shadow: 0 0 0 0.2rem rgba(82, 88, 93, 0.5);
    }

    &.disabled, &:disabled {
      color: #fff;
      background-color: #343a40;
      border-color: #343a40;
    }
  }

  //!BUTTONS!
  //SCROLL
  ::-webkit-scrollbar {
    width: 5px;
    height: 5px;
  }

  ::-webkit-scrollbar-button {
    width: 0px;
    height: 0px;
  }

  ::-webkit-scrollbar-thumb {
    background: #e1e1e1;
    border: 0px none #ffffff;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #ffffff;
  }

  ::-webkit-scrollbar-thumb:active {
    background: #b9cdda;
  }

  ::-webkit-scrollbar-track {
    background: #666666;
    border: 0px none #ffffff;
    //border-radius: 50px;
  }

  ::-webkit-scrollbar-track:hover {
    background: #666666;
  }

  ::-webkit-scrollbar-track:active {
    background: #333333;
  }

  ::-webkit-scrollbar-corner {
    background: transparent;
  }

  //!SCROLL!
  .breadcrumb-container {
    margin: 1rem 0;

    .breadcrumb {
      display: flex;
      flex-wrap: nowrap;
      background: none;
      margin: 0;
      padding: 0;
      list-style: none;
      border-radius: .25rem;
      white-space: nowrap;
      overflow-x: auto;
      @extend %_scroll-hide;

      &-item {
        a {
          @include link;
        }

        span {
          color: var(--text-second);
        }

        @include fz(14);

        &:before {
          color: var(--text-light) !important;
        }
      }
    }
  }

  fieldset {
    span {
      @include fz(14);
      color: var(--background-danger);
    }
  }


  .vue-skeleton-loading {
    .square {
      background-color: var(--card-background-preload) !important;
    }
  }

  .v-select {

    .vs__dropdown-toggle {
      border-color: var(--input-border);
    }

    .vs__actions {
      svg {
        color: var(--input-action);
        fill: var(--input-action);
      }
    }

    .vs__selected-options {
      * {
        color: var(--text-main);
      }
    }
    .vs__dropdown-option {
      &, * {
        color: var(--text-main);
        background-color: var(--input-background) !important;
      }
    }
    .vs__dropdown-menu{
      &, * {
        color: var(--text-main);
        background-color: var(--background-content) !important;
      }
    }
    input::placeholder {
      color: var(--text-muted);
    }
  }

</style>
