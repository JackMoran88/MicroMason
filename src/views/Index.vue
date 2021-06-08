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
          :crop="IS_MOBILE ? 'mobile' : 'standard'"
        />
         <div v-if="IS_MOBILE" >
            <span></span>
          </div>
        <v-btn
          v-if="IS_MOBILE"
          v-b-modal.catalogModal
          BtnName="Каталог товаров"
          BtnStyle="success"
          class="w-100"
        />
        <v-custom-products-line
          class="no-effect"
          title="Новинки"
          :data="PRODUCTS_LAST.queryset"
          :preloading="!PRODUCTS_LAST.load"
        />
        <v-custom-products-line
          class="no-effect"
          title="Популярные товары"
          :data="PRODUCTS_POPULAR.queryset"
          :preloading="!PRODUCTS_POPULAR.load"
        />
        <v-viewed-products
          class="no-effect"
        />

        <v-custom-products-line
          class="no-effect"
          title="Самые желаемые товары"
          :data="PRODUCTS_POPULAR_WISH.queryset"
          :preloading="!PRODUCTS_POPULAR_WISH.load"
        />
      </div>

    </v-grid>

  </div>
</template>

<script>
  import {mapActions, mapGetters, mapMutations} from 'vuex';
  import vDropCatalogMain from '@/components/app/catalog/v-drop-catalog-main.vue';

  export default {
    name: 'Index',
    components: {
      vDropCatalogMain,
    },
    methods: {
      load() {
        this.GET_PRODUCTS_QUERYSETS({type: 'last'}).then((data) => {
          this.SET_PRODUCT_LAST_TO_STATE(data)
        })
        this.GET_PRODUCTS_QUERYSETS({type: 'popular'}).then((data) => {
          this.SET_PRODUCT_POPULAR_TO_STATE(data)
        })
        this.GET_PRODUCTS_QUERYSETS({type: 'popular_wish'}).then((data) => {
          this.SET_PRODUCT_POPULAR_WISH_TO_STATE(data)
        })
      },
      ...mapActions(['GET_PRODUCTS_QUERYSETS']),
      ...mapMutations(['SET_PRODUCT_LAST_TO_STATE', 'SET_PRODUCT_POPULAR_TO_STATE', 'SET_PRODUCT_POPULAR_WISH_TO_STATE',])
    },
    computed: {
      ...mapGetters(['IS_MOBILE', 'IS_DESKTOP', 'PRODUCTS_LAST', 'PRODUCTS_POPULAR', 'PRODUCTS_POPULAR_WISH']),
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
