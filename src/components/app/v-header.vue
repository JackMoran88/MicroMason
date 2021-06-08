<template>
  <section class="header">
    <nav class="header__content container"
         v-if="IS_DESKTOP"
    >
      <div class="header__content-top">
        <div class="header__content-top-item__left">
          <a class="header__item"
             v-if="SETTINGS && SETTINGS.phone"
             :href="`tel:${SETTINGS.phone}`">{{SETTINGS.phone}}</a>
        </div>
        <v-theme-switcher
          class="header__content-top-item mr-auto"
        />
        <div class="header__content-top-item__right">
          <v-btn
            BtnStyle="secondary"
            @click.native="IS_LOGGED_IN ? logout() : $bvModal.show('authModal')"
            :BtnName="IS_LOGGED_IN ? '': 'Вход'"
            class="header__item"
          />
          <v-dropdown
            v-if="IS_LOGGED_IN"
            :data="USER_DROP_DATA"
            class="header__item"
          />
        </div>
      </div>
      <div class="header__content-middle">
        <router-link class="header__brand" to="/">MicroMason</router-link>
        <v-btn
          @click.native="toggleCategory"
          class="header__burger"
          BtnIcon="menu"
          BtnStyle="header-burger"
        />
        <header-search
          class="header__search"
        />
        <div class="header__actions">
          <router-link :to="{name:'Account comparison'}">
            <header-compare
              class="header__actions-item"
            />
          </router-link>
          <router-link :to="{name:'Account wish'}">
            <header-wish
              class="header__actions-item"
            />
          </router-link>
          <header-cart
            v-b-modal.cartModal
            :CartCount="CART_IDS.length"
            class="header__actions-item"
          />
        </div>
      </div>

    </nav>

    <nav class="header__content__mobile container"
         v-if="IS_MOBILE"
    >
      <v-btn
        v-if="IS_MOBILE"
        BtnIcon="menu"
        BtnStyle="header-burger"
        class="header__burger"
        v-b-toggle.mobileMenu

      />

      <header-search
        class="header__search"
      />

      <header-cart
        v-if="IS_MOBILE"
        class=""
        v-b-modal.cartModal
        :CartCount="CART_IDS.length"
      />
    </nav>

    <v-mobile-menu
      :menu="USER_DROP_DATA"
    />

  </section>

</template>

<script>
  import {eventBus} from '@/main';
  import {mapGetters} from 'vuex';

  export default {
    name: 'v-header',

    data() {
      return {
        isMobileCategory: false,
      };
    },
    components: {
      vDropdown: () => import('@/components/popup/v-dropdown.vue'),
      vMobileMenu: () => import('@/components/app/mobile/slideMenu.vue'),
      vThemeSwitcher: () => import('@/components/app/v-theme-switcher.vue'),
    },
    methods: {
      toggleCategory() {
        eventBus.$emit('toggleCategory');
      },
      logout() {
        this.$store.dispatch('LOGOUT');
      },
    },
    computed: {
      ...mapGetters(['CART_IDS', 'SETTINGS', 'IS_MOBILE', 'IS_DESKTOP', 'IS_LOGGED_IN', 'USER_DROP_DATA']),
    },
  };

</script>

<style scoped lang="scss">

  .header {
    display: flex;
    justify-content: center;
    background: var(--background-dark);
    padding: 0;
    width: 100%;
    max-width: 100%;

    z-index: 99;

    &__content {
      display: flex;
      flex-direction: column;
      padding: 0 1rem;
      z-index: 40;

      > * {
        margin: .25rem 0;
      }

      &-top {
        display: flex;
        justify-content: space-between;
        margin: .25rem .7rem 0 .7rem;

        > * {
          display: flex;
          width: fit-content;
        }

        &-item {
          align-items: center;

          &__left {
            .header__item {
              padding-right: 1rem;
            }
          }

          &__right {
            .header__item {
              padding-left: 1rem;
            }
          }
        }


      }

      &-middle {
        display: flex;
      }

      .header__search {
        flex-grow: 1;
        margin: 0 5rem;
      }
    }

    &__content__mobile {
      display: flex;
      justify-content: space-between;
      padding: 0 .5rem;

      /*Для открывающегося поиска*/
      position: relative;


      .header__search {
        flex-grow: 1;
        margin: 0 1rem;
      }
    }

    &__item {
      display: flex;
      align-self: center;
      color: white !important;
      padding: 0;

    }

    &__brand {
      color: white;
      padding-right: 1rem;
      margin: 0 0 0 .7rem;
      font-size: 2.2rem;

    }

    &__actions {
      display: flex;

      &-item {
        margin: .2rem .7rem;
      }
    }
  }

  .dropdown {
    width: 100%;
    padding: .2rem .5rem;
    color: var(--background-dark-second);

    &__btn {
      width: 100%;
      cursor: pointer;
      font-style: normal;
      text-transform: uppercase;
      position: relative;

      div {
        width: 100%;

        a {
          color: var(--background-dark-second);
        }
      }

      i {
        position: absolute;
        top: 0;
        right: 0;
        height: 100%;

        display: flex;
        align-items: center;
      }
    }

    &__content,
    &__content a, &__content button {
      display: flex;
      justify-items: center;
      flex-direction: column;
      text-indent: 5px;

      p {
        padding: .2rem;
        margin: 0;

        a {
          color: var(--background-dark-second);
        }
      }
    }

  }

</style>
