<template>
  <button
    class="btn card-btn"
    :class="{'fill': WISH_IDS && WISH_IDS.includes(ProductId)}"
    @click="click"
    aria-label="button"
  ></button>
</template>

<script>
  import {mapGetters, mapActions} from 'vuex';

  export default {
    name: 'v-btn-wish',
    components: {},
    data() {
      return {};
    },
    props: {
      ProductId: {
        type: Number,
      },
    },
    methods: {
      click() {
        if (this.WISH_IDS && this.WISH_IDS.includes(this.ProductId)) {
          this.DELETE_WISH(this.ProductId);
          this.$toast('info', 'Товар удален из избранного!')
        } else {
          this.ADD_WISH(this.ProductId);
          this.$toast('info', 'Товар добавлен в избранное!')
        }
      },
      ...mapActions(['ADD_WISH', 'DELETE_WISH']),
    },
    computed: {
      ...mapGetters(['WISH_IDS', 'IS_LOGGED_IN', 'authStatus']),
    },
  };
</script>

<style scoped lang="scss">
  button {
    z-index: 12;
    @include fz(26px);
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

</style>
