<template>
  <section class="cart">
    <div class="cart-list" v-if="CART.length">
      <v-cart-item
        v-for="product in CART"
        :key="product.id"
        :Product="product"
        @changeQty="changeQty"
      />

    </div>
    <div class="cart-footer" v-if="CART.length">
      <div class="cart-footer-total">Всего: {{totalPrice | formattedPrice}} ₴</div>
      <v-btn
        v-if="!checkout"
        BtnName="Оформить заказ"
        @click.native="$router.push({name: 'Checkout'}, () => {})"
        BtnStyle="success"
      />
    </div>
    <div class="cart-empty" v-if="!CART.length">
      <div class="cart-empty__title">
        <i>shopping_cart</i>
        <v-title
          text="Корзина пуста"
        />
      </div>
      <v-viewed-products/>
    </div>
  </section>
</template>

<script>
  import vCartItem from '@/components/app/cart/v-cart-item.vue';
  import {mapActions, mapGetters} from 'vuex';
  import formattedPrice from '@/filters/formatPrice';
  import vViewedProducts from '@/components/app/container/v-viewed-products.vue';

  export default {
    name: 'v-cart',
    components: {
      vCartItem, vViewedProducts,
    },
    props: {
      checkout: {
        type: Boolean,
        default: false,
      },
    },
    filters: {
      formattedPrice,
    },
    data() {
      return {
        products: [],
        totalPrice: 0,
      };
    },
    methods: {
      changeQty(productId, quantity) {
        this.ADD_TO_CART({product: productId, quantity})
          .then(() => {
            this.getProducts();
          });
      },
      getProducts() {
        this.GET_CART_DETAIL()
          .then(() => {
            this.totalPrice = 0;
            this.CART.forEach((product) => {
              this.totalPrice += product.totals;
            });
          });
      },
      ...mapActions(['ADD_TO_CART', 'GET_CART_DETAIL', 'GET_PRODUCTS_BY_IDS']),
    },
    computed: {
      ...mapGetters(['CART', 'PRODUCT']),
    },
    mounted() {
      this.getProducts();
    },
    watch: {
      $route() {
        this.$bvModal.hide('cartModal');
      },
      //Если добавить товар через корзину в просмотренных
      'CART.length'() {
        this.getProducts()
      }
    },
  };
</script>

<style lang="scss">

  //Cart
  .cart-empty {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;

    &__title {
      display: flex;
      flex-direction: column;
      margin: 5rem 0;

      i {
        @extend %_material-icons;
        display: flex;
        justify-content: center;
        font-size: 144px;
      }
    }
  }

  section.cart {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;

    .cart-list {
      display: flex;
      flex-direction: column;
      overflow-y: auto;
    }

  }

  .cart-footer {
    position: sticky;
    bottom: 0;
    background: var(--background-content);

    display: flex;
    justify-content: flex-end;
    padding: 1rem 0;
    z-index: 20;
    box-shadow: 0px -10px 20px 0px rgba(var(--background-light), 1);

    &-total {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 1rem;
      font-weight: 500;
      @include fz(20)

    }
  }

  //!Cart!
</style>
