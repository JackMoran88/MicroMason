<template>

  <section class="quick-view">
    <v-gallery
      v-if="loaded"
      :slides="PRODUCT_SLIDES"
      :Product="PRODUCT"
    />
    <v-product-info
      :Product="PRODUCT"
    />
    <v-product-tab-spec
      :ProductSpecs="PRODUCT.options"
    />
  </section>

</template>

<script>
  import vProductInfo from '@/components/product/boards/v-product-info.vue';
  import vGallery from '@/components/product/boards/v-gallery.vue';
  import {mapActions, mapGetters} from 'vuex';
  import vProductTabSpec from '@/components/product/tabs/v-product-tab-spec.vue';

  export default {
    name: 'v-quick-view',
    components: {
      vProductInfo, vGallery, vProductTabSpec,
    },
    props: {
      ProductSlug: {
        type: String,
      },
    },
    data() {
      return {
        product: null,
        loaded: false,
        slides: [],
      };
    },

    methods: {
      ...mapActions(['GET_PRODUCT', 'SOCKET_SEND_MESSAGES']),
    },
    computed: {
      ...mapGetters(['PRODUCT', 'PRODUCT_SLIDES']),
    },
    mounted() {
      this.GET_PRODUCT(this.ProductSlug).then(() => {
        try {
          this.SOCKET_SEND_MESSAGES(['Product']);
        } catch {}
        this.loaded = true;
      });
    },
  };
</script>

<style lang="scss">
  .quick-view {
    display: flex;
    flex-direction: column;
    max-width: 100%;

    .quantity {
      display: none !important;
    }

    .product__slider {
      position: static !important;
    }
  }

</style>
