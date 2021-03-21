<template>
    <div class="v-filter-brand">
        <label
                v-for="brand in FILTERS.filters.brands"
                :key="brand.id"
        >
            <p-check
                    class="p-default"
                    color="primary"
                    v-model="brands"
                    :value="brand.name"
            >{{brand.name}}</p-check>
        </label>
    </div>
</template>

<script>
import PCheck from 'pretty-checkbox-vue/check';
import { mapGetters } from 'vuex';

export default {
  name: 'v-filter-brand',
  components: {
    PCheck,
  },
  data() {
    return {
      brands: [],
    };
  },
  methods: {
    load() {
      if (this.$route.query.brand) {
        this.brands = this.$route.query.brand.split(',');
      }
      if (this.brands.length) {
        this.change();
      }
    },
    change() {
      const data = {
        brand: this.brands.toString(),
      };
      this.$change_query_url(data);
      this.$submitFilters();
    },
  },
  computed: {
    ...mapGetters(['FILTERS']),
  },
  mounted() {
    this.load();
  },
  watch: {
    brands() {
      this.change();
    },
  },
};
</script>

<style scoped lang="scss">
    label {
        width: 100%;
        margin: 0;
        padding: 0 .25rem;

        input {
            margin-right: .25rem;
        }
    }

</style>
