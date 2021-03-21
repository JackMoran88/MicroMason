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
  </section>

</template>

<script>
import vProductInfo from '@/components/product/boards/v-product-info.vue';
import vGallery from '@/components/product/boards/v-gallery.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'v-quick-view',
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
  components: {
    vProductInfo, vGallery,
  },

  methods: {
    ...mapActions(['GET_PRODUCT', 'SOCKET_SEND_MESSAGES', 'SOCKET_CATCH']),
  },
  computed: {
    ...mapGetters(['PRODUCT', 'PRODUCT_SLIDES']),
  },
  mounted() {
    this.GET_PRODUCT(this.ProductSlug).then(() => {
      this.SOCKET_SEND_MESSAGES(['Product']);
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
