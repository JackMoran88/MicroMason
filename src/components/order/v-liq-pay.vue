<template>
    <form method="POST" accept-charset="utf-8" action="https://www.liqpay.ua/api/3/checkout" target="_blank">
        <input type="hidden" name="data"
               :value="data"/>
        <input type="hidden" name="signature"
               :value="signature"/>
        <v-btn
                BtnIcon="payment"
                BtnName="Оплатить"
                @click.native=""
                BtnStyle="success outline"
                BtnType="submit"
                class="w-fc"
        />
    </form>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'v-liq-pay',
  props: {
    order_id: {
      type: Number,
    },
  },
  data() {
    return {
      data: '',
      signature: '',
    };
  },
  methods: {
    load() {
      this.GET_LIQPAY_DATA(this.order_id).then((response) => {
        this.data = response.data;
        this.signature = response.signature;
      });
    },
    ...mapActions(['GET_LIQPAY_DATA']),
  },
  mounted() {
    this.load();
  },

};
</script>

<style scoped lang="scss">

  form{
    button{
      width: 100%;
    }
  }

</style>
