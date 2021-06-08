<template>

  <div class="v-card-line"
       v-dragscroll.x="!IS_MOBILE"
       @dragscrollstart="onDragStart"
       @click.capture="onDragClick"
  >
    <v-card-preloader
      v-if="preloading"
      v-for="i in 10"
    />

    <v-card
      v-if="!preloading && Products.length"
      v-for="product in Products"
      :Product="product"
    />
  </div>

</template>

<script>
  import vCard from '@/components/app/card/v-card';
  import {
    mapGetters, mapActions, mapMutations, mapState,
  } from 'vuex';
  import {dragscroll} from 'vue-dragscroll';

  export default {
    name: 'v-card-line',
    components: {
      vCard,
    },
    props: {
      Products: {},
      preloading:{
        type: Boolean,
        default: false,
      }
    },
    directives: {
      dragscroll,
    },
    data: () => ({
      dragged: false,
      dragTimeout: null,
    }),
    methods: {
      load() {

      },
      // Fix click after drag
      onDragStart() {
        clearTimeout(this.dragTimeout);
        this.dragged = false;
        this.dragTimeout = setTimeout(() => {
          this.dragged = true;
        }, 100); // Minimal delay to be regarded as drag instead of click
      },
      onDragClick(e) {
        if (this.dragged) {
          e.preventDefault();
        }
        this.dragged = false;
      },

      ...mapActions(['GET_PRODUCTS_BY_IDS']),
    },
    computed: {
      ...mapGetters(['IS_MOBILE']),
    },
    mounted() {

    },
  };
</script>

<style lang="scss">


  .v-card-line {
    display: flex;
    flex-wrap: nowrap;
    width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    @extend %_scroll-hide;

    .card {
      min-width: 200px;
      max-width: 200px;

      &:hover {
        transform: none !important;
      }

      .btn-compare, .btn-quick-view, .card__reviews .star-line__count {
        display: none;
      }
    }

  }

  @media (max-width: 768px) {
    .v-card-line {
      .card {
        min-width: 230px;
        max-width: 250px;
      }
    }
  }

  @media (max-width: 576px) {
    .v-card-line {
      .card {
        min-width: 50%;
        max-width: 50%;
      }
    }
  }

</style>
