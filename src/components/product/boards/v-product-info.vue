<template>
    <section class="v-product-info">
        <v-product-available
                :Product="Product"
        />
        <v-product-price
                :Product="Product"
        />
        <v-product-shipping/>
    </section>
</template>

<script>
import vProductShipping from '@/components/product/boards/v-product-shipping.vue';
import vBtnWish from '@/components/app/button/v-btn-wish.vue';
import vProductAvailable from '@/components/product/boards/v-product-available.vue';
import vProductPrice from '@/components/product/boards/v-product-price.vue';
import {
  mapGetters, mapActions, mapMutations, mapState,
} from 'vuex';

export default {
  name: 'v-product-info',
  components: {
    vProductShipping, vBtnWish, vProductAvailable, vProductPrice,
  },
  props: {
    Product: {
      // type: Object,
    },
  },
  methods: {},
  computed: {},
  mounted() {

  },
};
</script>

<style scoped lang="scss">

    i {
        @extend %_material-icons;
        font-size: 24px;
    }
</style>

<style lang="scss">

    .product__slider {
        position: sticky !important;
        top: 40px;
    }

    .product__board{
        @include def-border($color: var(--product-board-border), $border: true);
        margin: .75rem 0;
        padding: .25rem;
        width: 100%;
        background: var(--background-content);
        &__bg{
            background: var(--product-board-bg);
            @extend %_shadow;
        }
        &__diff-padding {
            max-width: 100%;
            overflow: auto;
            padding: 0;
            > * {
                padding: .5rem;
            }
        }

        > table {
            padding: 0 !important;
            border-spacing: .5rem 1rem;
            @include fz(14);
        }

        &__header {
            text-transform: uppercase;
            @include fz(16);
            font-weight: 500;
            border-bottom: 1px solid var(--product-board-border);
            background: var(--product-board-bg);
        }
        &__body{

        }
        &__footer{

        }
        &__header, &__body, &__footer{
            &.reverse{
                display: flex;
                align-items: center;
                flex-direction: row-reverse;
            }
        }
    }

    .a {

    }
</style>
