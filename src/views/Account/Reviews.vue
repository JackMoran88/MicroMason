<template>
  <div id="account-reviews">
    <v-title
      text="Отзывы"
    />
    <div v-if="USER_REVIEWS.length">
      <v-review
        v-for="review in USER_REVIEWS" :key="review.id"
        :review="review"
      />
    </div>

    <v-attention
      v-if="!USER_REVIEWS.length"
      text="Вы еще не оставляли отзывов"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import vReview from '@/../src/components/review/v-review.vue';

export default {
  name: 'v-reviews',
  components: { vReview },
  data() {
    return {
      ParentId: null,
      ProductId: null,
    };
  },
  methods: {
    load() {
      this.GET_USER_REVIEWS();
    },
    ...mapActions(['GET_USER_REVIEWS']),
  },
  computed: {
    ...mapGetters(['USER_REVIEWS']),
  },
  mounted() {
    this.load();
  },
  watch: {},
};
</script>

<style scoped lang="scss">

</style>
