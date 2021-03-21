<template>

  <div id="account-orders">
    <v-title
      text="Заказы"
    />
    <div v-if="ORDERS.length">
      <v-order
        v-for="order in ORDERS" :key="order.id"
        :order="order"
      />
    </div>
    <v-attention
      v-if="!ORDERS.length"
      text="Ваш список заказов - пуст"
    />
  </div>

</template>

<script>
import vOrder from '@/../src/components/order/v-order.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'Orders',
  components: {
    vOrder,
  },
  methods: {
    ...mapActions(['GET_ORDERS']),
  },
  computed: {
    ...mapGetters(['ORDERS']),
  },
  mounted() {
    this.GET_ORDERS();
  },
};
</script>

<style scoped lang="scss">

</style>
