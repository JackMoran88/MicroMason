<template>
  <div>

    <b-sidebar id="mobileMenu" shadow backdrop no-header #default="{ hide }">
      <div class="header">
        <router-link to="/"><strong>MicroMason</strong></router-link>
        <i @click="hide" class="close">close</i>
      </div>
      <div class="userline">
        <ul class="userline__nav">
          <span><a class="userline__nav-link" href="tel:38000000000">38000000000</a></span>
        </ul>
        <ul class="userline__nav">
          <v-theme-switcher
            class="header__content-top-item mr-auto"
          />
          <li class="userline__nav-link user" v-b-modal.authModal v-if="!IS_LOGGED_IN">
            <span>Вход</span>
          </li>
          <li class="userline__nav-link user h9P" @click="logout" v-else>
            <span>Выход</span>
          </li>
        </ul>

        <div class="mobile-user-nav">
          <div class="active" v-b-modal.catalogModal>
            <i>view_list</i>
            <span>Каталог товаров</span>
          </div>
          <a v-for="item in menu.items" @click="click(item)">
            <div>
              <i>{{item.icon}}</i>
              <span>{{item.text}}</span>
            </div>
          </a>

        </div>

      </div>
    </b-sidebar>
  </div>
</template>

<script>
  import {eventBus} from '@/main';
  import {
    mapGetters, mapActions, mapMutations, mapState,
  } from 'vuex';
  import vThemeSwitcher from '@/components/app/v-theme-switcher.vue';

  export default {
    name: 'slideMenu',
    props: {
      menu: {
        type: Object,
      },
    },
    components: {
      vThemeSwitcher,
    },
    methods: {
      logout() {
        this.$store.dispatch('LOGOUT');
      },
      click(item) {
        if (this.IS_LOGGED_IN){
          this.$router.push(item.link.href)
        }
        else if (!item.isAuth) {
          this.$router.push(item.link.href)
        } else if (item.isAuth && !this.IS_LOGGED_IN) {
          this.$bvModal.show('authModal')
        }
      },
    },
    computed: {
      ...mapGetters(['IS_LOGGED_IN']),
    },
  };
</script>

<style lang="scss">

  #mobileMenu {
    i {
      @extend %_material-icons;
      font-size: 24px;

      &.close {
        color: var(--modal-close);
        text-shadow: none;
        opacity: 1;
      }
    }

    z-index: 45;
    @include list-style-off;

    .b-sidebar-body, .b-sidebar-header {
      background: var(--background-dark);
      color: white;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: .5rem 0;

      a {
        color: white;

        strong {
          @include fz(34px);
        }
      }
    }

    .b-sidebar-body {
      padding: 0 1rem;
    }

    .userline {
      &__nav {
        padding: .25rem 0;
        margin: 0;
        display: flex;
        justify-content: space-between;

        &-link {
          color: white;
        }
      }
    }

    .mobile-user-nav {
      padding: 1rem 0;

      a, & {
        width: 100%;

        > div {
          display: flex;
          align-items: center;
          color: white;
          padding: .7rem 0;
          @include fz(20px);

          i {
            color: var(--text-second);
            padding-right: .5rem;
          }
        }
      }

      .active {
        * {
          color: var(--accent);
        }
      }
    }
  }

</style>
