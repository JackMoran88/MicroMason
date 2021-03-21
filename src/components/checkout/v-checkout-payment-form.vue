<template>
  <v-account-form
    @toggle="close"
    :actions="false"
    :state="true"
  >
    <div slot="header">
      <div class="form__title"><span>payment</span>Способ оплаты</div>
    </div>
    <div slot="body">
      <v-select
        v-if="PAYMENT.length > 0"
        placeholder="Способ оплаты"
        @option:selected="changePayment"
        :options="payment_options"
        :clearable="false"
      />


      <div class="form__note" v-if="$search_by(PAYMENT, 'id', curPayment)">
        {{$search_by(PAYMENT, 'id', curPayment).description}}
      </div>
    </div>

  </v-account-form>
</template>

<script>
  import {mapActions, mapGetters, mapMutations} from 'vuex';
  import vAccountForm from '@/components/app/form/v-account-form.vue';

  export default {
    name: 'v-checkout-payment-form',
    components: {
      vAccountForm,
    },
    data() {
      return {
        curPayment: null,
        payment_options: [],
      };
    },
    methods: {
      load() {
        this.GET_PAYMENT().then(() => {
          if (this.PAYMENT.length) {
            this.curPayment = this.PAYMENT[0].id;
            this.loadPaymentOptions()
          }
        });
      },
      loadPaymentOptions() {
        this.payment_options = this.PAYMENT.map((value) => {
          return {
            label: `${value.name}`,
            value: value.id
          }
        })
      },
      changePayment(select) {
        this.curPayment = select.value;
        this.SET_CHECKOUT_PAYMENT(this.curPayment);

      },
      close() {
        this.load();
      },
      ...mapActions(['GET_PAYMENT']),
      ...mapMutations(['SET_CHECKOUT_PAYMENT'])
    },
    computed: {
      ...mapGetters(['PAYMENT']),
    },
    mounted() {
      this.load();
    },
    watch: {},
  };
</script>

<style scoped lang="scss">
  .v-select {
    margin: .5rem 0;
  }
</style>
