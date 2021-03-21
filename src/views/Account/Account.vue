<template>
  <div class="w-100">
    <Breadcrumbs/>
    <div class="account">
      <ul class="account__menu">
        <div class="account__menu-header">
          <router-link :to="{name:'Account main'}" class="account__menu-item">
            <i class="account__menu-header-photo">account_circle</i>
            <div class="account__menu-header-info">
              <a>{{FULL_USER_NAME}}</a>
              <p v-if="USER && USER.email">{{USER.email}}</p>
            </div>
          </router-link>
        </div>
        <div class="account__menu-body" v-if="IS_LOGGED_IN">
          <router-link :to="{name:'Account wish'}" class="account__menu-item">
            <i>favorite_border</i>
            <span>Мои закладки</span>
          </router-link>
          <router-link :to="{name:'Account orders'}" class="account__menu-item">
            <i>toc</i>
            <span>Мои заказы</span>
          </router-link>
          <router-link :to="{name:'Account reviews'}" class="account__menu-item">
            <i>rate_review</i>
            <span>Мои отзывы</span>
          </router-link>
          <router-link :to="{name:'Account comparison'}" class="account__menu-item">
            <i>compare_arrows</i>
            <span>Мои сравнения</span>
          </router-link>
        </div>
      </ul>
      <div class="account__content">
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'Account',
  methods: {
    ...mapActions(['']),
  },
  computed: {
    ...mapGetters(['FULL_USER_NAME', 'USER', 'IS_LOGGED_IN']),
  },
  mounted() {

  },
};
</script>

<style scoped lang="scss">

  i {
    @extend %_material-icons-outlined;
    font-size: 24px;
  }

  .account {
    display: grid;
    grid-template-columns: minmax(250px, 250px) minmax(0, 100%);

    &__menu {
      display: flex;
      flex-direction: column;
      padding: 0;

      &-header {
        @extend %_shadow;
        @include def-border;
        padding: 0;
        display: flex;
        align-items: center;
        background: var(--background-content);
        cursor: pointer;
        margin-bottom: .5rem;
        overflow: hidden;

        p {
          color: var(--text-second);
          @include fz(12);
          margin: 0;

          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          width: fit-content;
        }

        i {
          max-width: 20%;
        }

        div {
          width: 80%;
          padding: 0 .5rem;
          overflow: hidden;
        }

        a {
          font-size: 14px;
        }
      }

      &-body {
        @extend %_shadow;
        background: var(--background-content);
        border-radius: 7px;
        overflow: hidden;

      }

      &-item {
        display: flex;
        align-items: center;
        padding: .3rem;
        border: 0;
        color: var(--link);
        width: 100%;

        &:hover {
          color: var(--link-hover);

          > i {
            color: var(--link-hover);
          }
        }

        span {
          padding: 0 .5rem;
        }

        i {
          @include def-border;
          padding: .25rem;
          background: var(--background-light);
          color: var(--text-main);
          border-radius: 25px;
        }
      }
    }

    &__content {
      padding: 0 2rem;
    }

    .router-link-exact {
      &-active {
        //background: var(--background-light);
        background-color: rgba(var(--background-dark), .05);
        border-radius: 7px;
        border: 1px solid rgba(var(--background-dark), .05);
      }
    }
  }

  @media (max-width: 576px) {
    .account {
      grid-template-columns: 0 100%;

      &__content {
        padding: 0rem;
      }
    }

  }
</style>
