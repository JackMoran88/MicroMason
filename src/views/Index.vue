<template>
  <div id="index">
    <v-grid
      :leftW="`330px`"
      :centerW="`100%`"
      :isCenter="true"
      :isLeft="IS_DESKTOP"
    >
      <div slot="left">
        <v-drop-catalog-main
          class="static"
        />

      </div>
      <div slot="center">
        <v-slider
          place="home"
          crop="standard"
        />
        <v-custom-products-line
          class="no-effect"
          title="Новинки"
          :data="PRODUCTS_LAST"
        />
        <v-viewed-products
          class="no-effect"
        />
      </div>

    </v-grid>

  </div>
</template>

<script>
  import {mapActions, mapGetters} from 'vuex';
  import vDropCatalogMain from '@/components/app/catalog/v-drop-catalog-main.vue';

  export default {
    name: 'Index',
    components: {
      vDropCatalogMain,
    },
    methods: {
      load() {
        this.GET_PRODUCT_LAST()
      },
      ...mapActions(['GET_PRODUCT_LAST'])
    },
    computed: {
      ...mapGetters(['CATEGORIES', 'SLIDERS', 'IS_MOBILE', 'IS_DESKTOP', 'PRODUCTS_LAST']),
    },
    mounted() {
      this.load()
    },
  };
</script>

<style lang="scss" scoped>
  #index {
    width: 100%;
    height: 100%;
    display: flex;


    flex-direction: column;
  }

</style>
