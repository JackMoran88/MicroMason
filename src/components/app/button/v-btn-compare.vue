<template>
  <button
    class="btn btn-compare card-btn"
    :class="{'fill': COMPARE_IDS.includes(ProductId)}"
    @click="click"
    aria-label="button compare"
  ></button>
</template>

<script>
  import {mapGetters, mapActions} from 'vuex';

  export default {
    name: 'v-btn-compare',
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
      load() {

      },
      click() {
        if (this.COMPARE_IDS.includes(this.ProductId)) {
          this.DELETE_FROM_COMPARE(this.ProductId);
          this.$toast('info', 'Товар удален из сравнения!')
        } else {
          this.ADD_TO_COMPARE(this.ProductId);
          this.$toast('info', 'Товар добавлен в сравнение!')
        }
      },
      ...mapActions(['ADD_TO_COMPARE', 'DELETE_FROM_COMPARE']),
    },
    computed: {
      ...mapGetters(['COMPARE', 'COMPARE_IDS']),
    },
    mounted() {
      this.load();
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
</style>
