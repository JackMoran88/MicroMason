<template>
  <div class="wish">
    <v-title
      text="Список желаемого"
    />

    <v-attention
      v-if="WISH.results && !WISH.results.length"
      text="Ваш список желаемого - пуст"
    />
    <section class="category__body no-filter" v-else>
      <div class="category__body-list">
        <v-card
          v-for="product in WISH.results"
          :key="product.id"
          :Product="product"
        />

        <v-paginate
          style="grid-column: 1/end"
          v-if="WISH.paginate"
          v-show="WISH.paginate.count_page > 1"
          :PageCount="WISH.paginate.count_page"
          :Link="WISH.paginate.links.next || WISH.paginate.links.previous"
          :Current="WISH.paginate.current_page"
        />
      </div>
    </section>
  </div>
</template>

<script>
  import vCard from '@/components/app/card/v-card.vue';
  import {mapActions, mapGetters} from 'vuex';

  export default {
    name: 'Wish',
    components: {
      vCard,
    },
    methods: {
      load() {
        const data = {}
        if (this.$route.query.page) {
          data.page = this.$route.query.page;
        }
        this.GET_WISH(data)
      },
      ...mapActions(['GET_WISH']),
    },
    computed: {
      ...mapGetters(['WISH']),
    },
    mounted() {
      this.load();
    },
    watch: {
      '$route.query.page'() {
        this.load();
      },
    }

  };
</script>

<style scoped lang="scss">

  div.wish {
    width: 100%;
  }
</style>
