<template>
  <div class="v-filter-board">
    <slot name="header">
      <div class="d-flex" v-if="showFilters">
        <v-title
        text="Фильтры"
        type="second"
        class="mt-0"
      />
      <v-btn
        BtnName="Очистить"
        BtnStyle="item"
        style="color: red"
        @click.native="clearFilters"
      />
      </div>
    </slot>
    <v-filter-container name="Цена" v-if="showFilters"
    >
      <v-filter-price
        slot="default"
      />
    </v-filter-container>
    <div v-if="!onlyPrice">
      <v-filter-container
        v-for="filter in FILTERS.filters"
        :key="filter.id"
        :name="filter[0].name"
        :length="filter[1].choices.length"
        v-if="filter[0].name"
      >
        <v-filter-multiply
          slot="default"
          :data="filter[1].choices"
          :URLQuery="filter[0].request_name"
        />
      </v-filter-container>
    </div>
  </div>
</template>

<script>
  import {mapActions, mapGetters, mapMutations} from 'vuex';
  import vFilterContainer from '@/components/app/filter/v-filter-container.vue';
  import vFilterPrice from '@/components/app/filter/v-filter-price.vue';
  import vFilterBrand from '@/components/app/filter/v-filter-brand.vue';
  import vFilterMultiply from '@/components/app/filter/v-filter-multiply.vue';

  export default {
    name: 'v-filter-board',
    components: {
      vFilterPrice, vFilterContainer, vFilterBrand, vFilterMultiply,
    },
    props: {
      onlyPrice: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        price: '',
      };
    },
    methods: {
      load() {
        if (this.$route.params.slug) {
          this.GET_FILTERS(this.$route.params.slug);
        }
      },
      loadQueryFromUrl() {
        // Можно не писать, поскольку, это уже отрабатывает sort_by
      },
       clearFilters() {
        this.CLEAR_CHOICE_FILTER()
        this.$router.replace({query: null}).catch(() => {
        })
         this.$update_query_url()
      },
      ...mapActions(['GET_PRODUCTS', 'GET_FILTERS']),
      ...mapMutations(['CLEAR_CHOICE_FILTER'])
    },
    computed: {
      showFilters(){
        return this.FILTERS.filters && this.FILTERS.filters.prices &&  this.FILTERS.filters.prices[1] > 0
      },
      ...mapGetters(['FILTERS']),
    },
    mounted() {
      this.load();
    },
    watch: {
      $route() {
        this.load();
      },
    },
  };
</script>

<style scoped lang="scss">



  .v-filter-board {

    .v-filter-container {
      margin: .5rem 0;
    }
  }

</style>
