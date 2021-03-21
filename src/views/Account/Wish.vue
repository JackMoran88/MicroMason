<template>
  <div class="wish">
    <v-title
      text="Список желаемого"
    />
    <v-attention
      v-if="!WISH.length"
      text="Ваш список желаемого - пуст"
    />
    <section class="category__body no-filter" v-else>
      <div class="category__body-list">
        <v-card
          v-for="product in WISH"
          :key="product.id"
          :Product="product"
        />
      </div>

    </section>
  </div>
</template>

<script>
import vCard from '@/components/app/card/v-card.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'Wish',
  components: {
    vCard,
  },
  methods: {
    reload() {

    },
    ...mapActions(['GET_WISH']),
  },
  computed: {
    ...mapGetters(['WISH']),
  },
  mounted() {
    this.GET_WISH();
  },

};
</script>

<style scoped lang="scss">

  div.wish {
    width: 100%;
  }
</style>
