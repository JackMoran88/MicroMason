<template>
  <div class="v-filter-price">
    <v-input
      InputTitle="От"
      v-model="value[0]"
      :InputValue="value[0]"
      InputType='number'
      :InputNumberOnly="true"
      @change.native="change"
      ref="from"

    />
    <v-input
      InputTitle="До"
      v-model="value[1]"
      :InputValue="value[1]"
      InputType='number'
      :InputNumberOnly="true"
      @change.native="change"
      ref="to"
    />
    <vue-slider
      :min="minmax[0]"
      :max="minmax[1]"
      :step="100"

      :height="10"
      :dotSize="15"

      v-model="value"

      :dragOnClick="true"
      @drag-end="change"
      :silent="true"

      ref="slider"
    />
  </div>
</template>

<script>
  import VueSlider from 'vue-slider-component';
  import 'vue-slider-component/theme/antd.css';
  import {mapGetters} from 'vuex';

  export default {
    name: 'v-filter-price',
    components: {
      VueSlider,
    },
    data() {
      return {
        value: [0, 1000000],
        minmax: [0, 1000000],
      };
    },
    methods: {
      load() {
        this.getValuesFromRoute();
        this.fixRangeValue();
      },
      getValuesFromRoute() {
        if (this.$route.query.min_price) {
          this.$refs.slider.setValue([this.$route.query.min_price, this.value[1]]);
        }
        if (this.$route.query.max_price) {
          this.$refs.slider.setValue([this.value[0], this.$route.query.max_price]);
        }
      },
      getMinMaxFromFilter() {
        this.$set(this, 'minmax', this.FILTERS.filters.prices);
        this.$refs.slider.setValue([this.minmax[0], this.minmax[1]]);
      },
      fixRangeValue() {
        for (const num in this.value) {
          if (this.value[num] > this.minmax[1]) {
            this.value[num] = this.minmax[1];
          }
          if (this.value[num] < this.minmax[0]) {
            this.value[num] = this.minmax[0];
          }
        }
      },
      change() {
        const data = {
          min_price: this.value[0],
          max_price: this.value[1],
        };
        this.$change_query_url(data);
        this.$submitFilters();
      },
    },
    computed: {
      ...mapGetters(['FILTERS']),
    },
    mounted() {
      this.getMinMaxFromFilter();
      this.load();
    },
    watch: {
      '$route'() {
        this.getMinMaxFromFilter();
        this.load();
      },
      'FILTERS'() {
        this.load();
      },
      'value'() {
        this.fixRangeValue();
      },
    },
  };
</script>


<style lang="scss">
  $themeColor: #424E65;
  @import '~vue-slider-component/lib/theme/antd.scss';

  .v-filter-price {
    display: flex;
    flex-wrap: wrap;
    padding: .5rem 0;

    > * {
      &.v-input {
        max-width: 50%;
      }

      padding: 0 .25rem !important;
    }

    .vue-slider {
      width: calc(100% - 24px) !important;
      margin: 0 auto;
    }
  }

</style>
