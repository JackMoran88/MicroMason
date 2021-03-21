<template>
  <div class="checkout" v-if="!checkout_success">
    <v-title
      text="Оформление заказа"
      type="main"
    />

    <v-account-address-form
      ref="address_form"
    />

    <v-checkout-cart-form/>

    <v-checkout-shipping-form
      ref="shipping_form"
    />

    <v-checkout-payment-form
      ref="payment_form"
    />

    <v-account-form
      :actions="false"
      :state="true"
    >
      <div slot="header">
        <div class="form__title"><span>notes</span>Коментарий к заказу</div>
      </div>
      <div slot="body">
        <v-text-area
          AreaCols="5"
          :AreaModel="order_note"
          :InputValue="order_note"
          v-model="order_note"
          @blur="changeNote"
        />
      </div>
    </v-account-form>

    <v-btn
      BtnName="Заказ подтверждаю"
      BtnStyle="success"
      class="w-100"
      @click.native="MakeOrder"
    />
  </div>
  <div
    class="checkout"
    v-else>
    <v-title
      text="Ваш заказ успешно оформлен!"
      type="main"
    />
    <div
      v-if="RECEIPT"
      class="no-effect"
    >
      <v-title
        text="Благодарим вас за покупку в нашем магазине"
        type="second"
      />
      <p v-if="RECEIPT.id">Номер вашего заказа: {{RECEIPT.id}}</p>
      <p v-if="RECEIPT.status && RECEIPT.status.name">Статус вашего заказа:
        {{RECEIPT.status.name}}</p>
      <p v-if="RECEIPT.paid">Статус оплаты заказа: {{RECEIPT.paid}}</p>
      <p v-if="RECEIPT.shipping && RECEIPT.shipping.name">Способ доставки:
        {{RECEIPT.shipping.name}}</p>

      <v-liq-pay
        v-if="RECEIPT.payment_method.type === 'liqpay'"
        :order_id="RECEIPT.id"
      />
    </div>

    <v-viewed-products
      class="mt-auto no-effect"
    />

  </div>
</template>

<script>
  import vAccountForm from '@/components/app/form/v-account-form.vue';
  import vAccountAddressForm from '@/components/account/v-account-address-form.vue';
  import vCheckoutShippingForm from '@/components/checkout/v-checkout-shipping-form.vue';
  import vCheckoutPaymentForm from '@/components/checkout/v-checkout-payment-form.vue';
  import vCheckoutCartForm from '@/components/checkout/v-checkout-cart-form.vue';
  import vTextArea from '@/components/app/form/v-text-area.vue';
  import {mapActions, mapGetters, mapMutations} from 'vuex';

  export default {
    name: 'Checkout',
    components: {
      vAccountForm,
      vAccountAddressForm,
      vCheckoutShippingForm,
      vCheckoutPaymentForm,
      vCheckoutCartForm,
      vTextArea,
    },
    data() {
      return {
        isMethodAuth: true,

        checkoutData: '',
        checkout_success: false,

        order_note: '',
      };
    },
    methods: {
      changeNote() {
        this.SET_CHECKOUT_NOTE(this.order_note);
      },
      MakeOrder() {
        if (!this.CART.length) {
          this.$toast('error', 'Ваша корзина пуста');
          this.$scrollToTop();
          return 0;
        }
        if (!this.CHECKOUT.payment) {
          this.$toast('error', 'Выберите метод оплаты');
          this.$scrollToTop();
          return 0;
        }
        if (!this.CHECKOUT.shipping) {
          this.$toast('error', 'Выберите метод доставки');
          this.$scrollToTop();
          return 0;
        }
        if (!this.CHECKOUT.address) {
          this.$toast('error', 'Выберите адресс');
          this.$scrollToTop();
          return 0;
        }
        if (!this.CHECKOUT.branch) {
          this.$toast('error', 'Выберите отделение');
          this.$scrollToTop();
          return 0;
        }
        this.MAKE_ORDER().then(() => {
          this.checkout_success = true;
          this.$scrollToTop();
          this.GET_CART_DETAIL();
        });
        return 0;
      },
      ...mapMutations(['SET_CHECKOUT_NOTE', 'CLEAR_CHECKOUT']),
      ...mapActions(['GET_CUSTOMER_DETAIL', 'MAKE_ORDER', 'GET_CART_DETAIL', 'GET_LIQPAY_DATA']),
    },
    computed: {
      ...mapGetters(['USER', 'CART', 'CHECKOUT', 'RECEIPT']),
    },
    mounted() {
      this.GET_CUSTOMER_DETAIL(this.$store.getters.TOKEN);
      this.CLEAR_CHECKOUT()
    },
    watch: {
      CART() {
        if (!this.CART.length && !this.checkout_success) {
          this.$router.replace({name: 'Home'});
        }
      },
    },
  };
</script>

<style scoped lang="scss">
  .checkout {
    width: 100%;
    display: flex;
    flex-direction: column;

    > div {
      &:not(.no-effect) {
        background: var(--background-light);
        padding: .5rem 1rem !important;
        @include def-border();
        margin: 1rem 0;
      }
    }

    &__address {
      margin: 1rem 0;
      width: 100%;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      grid-column-gap: 1rem;

      .title {
        grid-column: 1/3;
      }
    }

    &__shipping {

    }
  }

</style>
