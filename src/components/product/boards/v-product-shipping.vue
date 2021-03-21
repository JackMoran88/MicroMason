<template>
  <div class="product-info__delivery product__board product__board__diff-padding"
       v-if="SHIPPING.length > 0">
    <div class="product__board__header">Доставка</div>
    <table class="product__board__body table">
      <tr>
        <th>Способ</th>
        <th>Описание</th>
        <th>Цена</th>
      </tr>
      <tr v-for="item in SHIPPING" :key="item.id">
        <td>{{item.name}}</td>
        <td>{{item.description}}</td>
        <td>{{item.price}} грн</td>
      </tr>
      <tr>
      </tr>
    </table>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'v-shipping',
  props: {},
  methods: {
    load() {
      this.GET_SHIPPING();
    },
    ...mapActions(['GET_SHIPPING']),
  },
  computed: {
    ...mapGetters(['SHIPPING']),
  },
  mounted() {
    this.load();
  },
};
</script>

<style scoped lang="scss">

</style>
