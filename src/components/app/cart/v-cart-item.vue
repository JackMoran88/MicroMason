<template>
  <div class="cart-item">
    <div class="cart-item-img">
      <img v-lazy="this.$store.state.backendUrl + Product.main_image.cart" :alt="Product.name">
    </div>
    <div class="cart-item-title">
      <router-link
        :to="{name: 'Product', params:{slug: Product.category_slug, ProductSlug: Product.slug}}"
        @click.native="$bvModal.hide('cartModal')"
      >
        <span>{{Product.name}}</span>
      </router-link>
    </div>
    <div class="cart-item-action">
      <v-more
        :ProductId="Product.id"
      />
    </div>
    <div class="cart-item-price">
      <quantity
        :Qty="Product.qty"
        @value="SetQtyItem"
      />
      <div class="price">
        <span>{{Product.totals | formattedPrice}}</span>
        <v-currency/>
      </div>
    </div>
  </div>
</template>

<script>
import vMore from '@/components/app/button/v-more.vue';
import formattedPrice from '@/filters/formatPrice';

export default {
  name: 'v-cart-item',
  components: {
    vMore,
  },
  filters: {
    formattedPrice,
  },
  props: {
    Product: {
      type: Object,
    },
  },
  methods: {
    SetQtyItem(value) {
      this.$emit('changeQty', this.Product.id, value);
    },
  },
};
</script>

<style scoped lang="scss">
  .cart-item {
    display: grid;
    grid-template-columns: 96px 1fr 96px;
    grid-template-rows: max-content min-content;
    margin: .25rem 0;
    padding: .25rem 0;
    border-bottom: 1px solid var(--background-light);

    &-img {
      img {
        max-width: 96px;
        height: 96px;
        flex-basis: 96px;
        object-fit: contain;
      }
    }

    &-title {
      width: auto;
      flex-grow: 1;
      margin: .2rem .7rem;
      height: 100%;
      @include fz(16);

      a {
        span {
          @include link()
        }
      }

    }

    &-action {
      display: flex;
      align-items: flex-start;
      justify-content: flex-end;
      width: 96px;
    }

    &-price {
      display: flex;
      justify-content: flex-end;
      min-width: 100%;
      padding: .25rem 1rem;
      grid-column: 1/last;

      .quantity {
        margin-left: auto;
        margin-right: 50px;
      }

      .price {
        min-width: 100px;
        text-align: end;

        span {

        }
      }
    }
  }

</style>
