<template>
  <div class="v-sort-by">
    <select @change="change(sortType)" v-model="sortType">
      <option
        v-for="option in options" :key="option.id" :value="option.field"
      >{{option.name}}
      </option>
    </select>
  </div>
</template>

<script>
  import {mapActions} from 'vuex';

  export default {
    name: 'v-sort-by',
    props: {
      options: {
        type: Array,
        default: () => [],
      },
      model: {
        type: Number,
      },
    },
    data() {
      return {
        sortType: 0,
        isOpen: true,
        current: '',
      };
    },
    methods: {
      load() {
        this.sortType = this.current;
      },
      toggle() {
        this.isOpen = !this.isOpen;
      },
      change(value) {
        this.$change_query_url({sort_by: value});

        const data = {
          slug: this.$route.params.slug,
          filters: this.$serialize_query(this.$route.query),
        };
        this.GET_PRODUCTS(data);
      },
      ...mapActions(['GET_PRODUCTS']),
    },
    created() {
      this.sortType = this.options[0].field;
      if (this.$route.query.sort_by) {
        this.current = this.$route.query.sort_by;
      } else {
        this.current = this.options[0].field;
      }
      this.load();
    },
  };
</script>

<style scoped lang="scss">

  .v-sort-by {
    display: flex;
    align-items: center;
    position: relative;
    margin-left: auto;
    align-self: flex-end;

    width: fit-content;
    select {
      border-radius: 4px;
      border-color: var(--background-light-second);
      background: var(--background-content) !important;
      color: var(--text-main);
      padding: .2rem .7rem;
      appearance: none;
      z-index: 2;
      background: transparent;
      padding-right: 30px;
    }

    &:before {
      @extend %_material-icons;
      font-size: 26px;
      content: 'keyboard_arrow_down';
      margin: 0 .15rem;
      height: min-content;
      position: absolute;
      width: 24px;
      right: 0;
      top: 4px;
      z-index: 5;
      color: var(--link);
      cursor: pointer;
    }
  }

</style>
