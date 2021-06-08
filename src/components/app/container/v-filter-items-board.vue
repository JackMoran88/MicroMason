<template>
  <div class="v-filter-items-board category__body">
    <div>
    </div>
    <div>
      <v-btn
        v-for="filter in filters"
        :BtnName="`${filter.param}: ${filter.name}`"
        BtnStyle="item"
        style="color: red"
        @click.native="removeFilter(filter)"
      />
    </div>
  </div>
</template>

<script>
  import {mapGetters, mapMutations} from "vuex";

  export default {
    name: "v-filter-items-board",
    data() {
      return {
        filters: []
      }
    },
    methods: {
      load() {
        this.getFilters()
      },
      getFilters() {
        let filters = []
        for (const [key, value] of Object.entries(this.CHOICE_FILTERS)) {
          value.forEach((v) => {
            filters.push({
              key: key,
              value: v,
              name: this.$search_by(this.FILTERS.filters[key][1].choices, 'id', parseInt(v)).name,
              param: this.FILTERS.filters[key][0].name,
            })
          })
        }

        this.filters = filters
      },
      removeFilter(filter) {
        let data = this.CHOICE_FILTERS[filter.key]
        data.splice(data.indexOf(filter.value), 1)
        this.SET_CHOICE_FILTER({key: filter.key, data: data})
      },
      ...mapMutations(['SET_CHOICE_FILTER', 'CLEAR_CHOICE_FILTER'])
    },
    computed: {
      ...mapGetters(['FILTERS', 'CHOICE_FILTERS']),
    },
    mounted() {
      this.load()
    },
    watch: {
      CHOICE_FILTERS: {
        handler(val) {
          this.getFilters()
        },
        deep: true
      }
    }

  }
</script>

<style scoped lang="scss">


</style>
