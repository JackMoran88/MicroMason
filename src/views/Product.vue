<template>
  <div class="w-100">
    <Breadcrumbs/>

    <div class="product__title">
      <v-title
        :text="PRODUCT.name"
      />
      <div class="product__title-review">
        <v-rating
          :Rating="PRODUCT.rating_avg"
          :CountReviews="PRODUCT.count_reviews ? PRODUCT.count_reviews : 0"
          @onClick="changeTab"
        />
      </div>
      <div class="product__title-code">Код: <span>{{PRODUCT.code}}</span></div>
    </div>

    <tabs
      :tabs="tabs"
      :currentTab="currentTab"
      :wrapper-class="'nav-tabs'"
      :tab-class="'nav-tabs__item'"
      :tab-active-class="'nav-tabs__item_active'"
      :line-class="'nav-tabs__active-line'"
      @onClick="changeTab"
    />

    <div id="tab-spec" class="product__tab"
         v-if="currentTab === 'tab-main' || currentTab === 'tab-spec'">
      <div class="product__image col-12 col-xl-6 col-sm-12">
        <v-gallery
          v-if="PRODUCT_SLIDES.length > 0 && gallery"
          :slides="PRODUCT_SLIDES"
          :Product="PRODUCT"
        />
      </div>

      <div class="product__info col-12 col-xl-6 col-sm-12">
        <v-product-info
          v-if="currentTab === 'tab-main'"
          :Product="PRODUCT"
        />
        <v-product-tab-spec
          v-if="currentTab === 'tab-spec'"
          :ProductSpecs="PRODUCT.options"
        />
      </div>
      <v-product-description
        :Product="PRODUCT"
      />
    </div>

    <v-tab-reviews
      v-if="currentTab === 'tab-review'"
      :ProductId="PRODUCT.id"
    />
    <v-custom-products-line
      class="no-effect"
      title="Товары категории"
      :data="PRODUCTS_FROM_CATEGORY.queryset"
      :preloading="!PRODUCTS_FROM_CATEGORY.load"
    />
    <v-viewed-products/>
  </div>
</template>

<script>
  import vGallery from '@/components/product/boards/v-gallery.vue';
  import vProductInfo from '@/components/product/boards/v-product-info.vue';
  import tabs from 'vue-tabs-with-active-line';

  import vProductTabSpec from '@/components/product/tabs/v-product-tab-spec.vue';
  import vTabReviews from '@/components/product/tabs/v-tab-reviews.vue';
  import vRating from '@/components/product/v-rating.vue';

  import vProductDescription from '@/components/product/boards/v-product-description.vue';

  import {mapActions, mapGetters, mapMutations} from 'vuex';

  export default {
    name: 'Product',
    props: ['ProductSlug', 'tab'],
    components: {
      vGallery,
      vProductInfo,
      tabs,
      vProductTabSpec,
      vTabReviews,
      vRating,
      vProductDescription,
    },
    data() {
      return {
        tabs: [
          {title: 'Всё о товаре', value: 'tab-main'},
          {title: 'Характиристики', value: 'tab-spec'},
          {title: 'Отзывы', value: 'tab-review'},
        ],
        currentTab: 'tab-main',
        gallery: false,
      };
    },
    methods: {
      setBreadCrumbs() {
        this.BREADCRUMBS({
          route: this.$route,
          breadcrumbs: this.$breadcrumbs,
        });
      },
      loadProduct() {
        this.GET_PRODUCT(this.ProductSlug).then(() => {
          this.setBreadCrumbs();

          this.ADD_VIEWED_PRODUCTS(this.PRODUCT.id);
          try{
            this.SOCKET_SEND_MESSAGES(['Product']);
          }catch{}

          this.currentTab = this.$route.meta.tab || 'tab-main';

          this.GET_PRODUCTS_QUERYSETS({type: 'popular_from_category', id: this.PRODUCT.category_id}).then((data) => {
            this.SET_PRODUCT_FROM_CATEGORY_TO_STATE(data)
          })
        });
      },
      changeTab(newTab) {
        let tab = '';
        switch (newTab) {
          case 'tab-main':
            tab = 'Product';
            break;
          case 'tab-spec':
            tab = 'Product characteristics';
            break;
          case 'tab-review':
            tab = 'Product review';
            break;
          default:
            tab = 'Product';
            break;
        }
        this.$scrollToTop();
        this.$router.replace({name: tab, params: {ProductSlug: this.ProductSlug}})
          .catch(() => {
          });
        this.currentTab = newTab;
      },

      ...mapActions(['GET_PRODUCT', 'BREADCRUMBS', 'ADD_VIEWED_PRODUCTS', 'CLEAR_PRODUCT', 'SOCKET_SEND_MESSAGES', 'GET_PRODUCTS_QUERYSETS']),
      ...mapMutations(['SET_PRODUCT_FROM_CATEGORY_TO_STATE',])
    },
    computed: {
      ...mapGetters(['PRODUCT', 'PRODUCT_SLIDES', 'PRODUCTS_FROM_CATEGORY']),
    },
    mounted() {
      this.loadProduct();
    },
    watch: {
      $route() {
        if (this.currentTab !== this.$route.meta.tab) {
          this.currentTab = this.$route.meta.tab || 'tab-main';
        }
      },
      '$route.params.ProductSlug'() {
        this.gallery = false;
        this.loadProduct();
      },
      PRODUCT_SLIDES() {
        this.gallery = false;
        this.gallery = true;
      },
    },
    metaInfo() {
      return {
        title: this.PRODUCT.name,
      };
    },
    destroyed() {
      this.CLEAR_PRODUCT()
    }
  };

</script>

<style scoped lang="scss">

  .product__title {
    display: flex;
    width: 100%;
    align-items: center;
    flex-wrap: wrap;
    justify-content: space-between;

    &-name {
      margin: 0;
      grid-column: 1/3;
    }

    &-review {
      white-space: nowrap;
    }

    &-code {
      overflow: hidden;
      height: 100%;
      text-align: right;
      color: var(--text-second);
      white-space: nowrap;

      span {
        color: dimgray;
      }
    }
  }

  .product {
    width: 100%;
    margin: 0;
    padding: .5rem 0;

    &__tab {
      width: 100%;
      display: flex;
      flex-wrap: wrap;
    }

    &__image {
      padding: 0;
    }
  }

  @media (max-width: 1200px) {
    .col-12, .col-sm-12 {
      padding: 0 !important;
    }
  }

</style>

<style lang="scss">

  /*TABS*/
  .nav-tabs {
    position: sticky;
    top: 0;
    z-index: 41;
    background: var(--background-content);
    border-color: var(--product-board-border);

    @extend %_scroll-hide;
    white-space: nowrap;
    overflow-x: auto;

    min-width: 100%;
    margin: .5rem 0 1rem 0;

    &__item {
      padding: .5rem;
      margin-right: 1rem;
      border: none;
      background: none;
      @include fz(14px);
      color: var(--text-main);

      &:hover {
        border-bottom: 2px solid var(--background-dark);
      }

      &:focus {
        outline: none !important;
      }

      &_active, &_active:hover {
        color: var(--accent);
        border-bottom: 2px solid var(--accent);
      }

    }

    &__active {
      &-line {
        display: none;

        height: 4px;
        background: var(--background-dark);
        border-radius: 1000px;
        margin: .05rem 0;
      }
    }
  }

  #tab-spec {
    margin: auto !important;
  }

</style>
