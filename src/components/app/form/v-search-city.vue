<template>
  <div class="v-search-city">
    <v-input
      InputTitle="Город"
      InputType='text'
      v-model="input"
      :InputValue="input"
      @InputBlur="blurInput()"
      @focus="isOpen = true"
      :InputErrors="InputErrors"
      :InputClass="InputClass"
    />

    <ul v-show="isOpen">
      <li
        v-for="city in cities.slice(0, 5)"
        @click="select(city.MainDescription)"
      >{{city.MainDescription}}
      </li>
    </ul>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  name: 'v-search-city',
  props: {
    InputTitle: {
      type: String,
      default: 'Поле',
    },
    InputId: {
      type: String,
      default: '',
    },
    InputClass: {
      type: Object,
      default: () => ({}),
    },
    InputModel: {
      type: String,
      default: '',
    },
    InputBlur: {
      type: String,
      default: '',
    },
    InputType: {
      type: String,
      default: 'text',
    },
    InputValue: {
      // type: String,
      default: '',
    },
    InputDisabled: {
      type: Boolean,
      default: false,
    },
    InputErrors: {
      type: Array,
      default: () => [],
    },
    InputNumberOnly: {
      type: Boolean,
      default: false,
    },
    InputNumberMax: {
      type: Number,
    },
    InputNumberMin: {
      type: Number,
    },
  },
  data() {
    return {
      input: '',
      cities: [],
      isOpen: false,
    };
  },
  methods: {
    load() {
      this.updValue();
    },
    updValue() {
      if (this.InputValue) {
        this.input = this.InputValue;
      }
    },
    search(query) {
      this.GET_CITY_BY_QUERY(query).then((response) => {
        this.cities = response.data[0].Addresses
        if (this.cities.length > 0 && this.isOpen) {
          this.cities.forEach((value) => {
            if (value.address === this.input) {
              this.cities = [];
            }
          });
          this.isOpen = true;
        }
      });
    },
    select(query) {
      this.$set(this, 'input', query);
    },
    close() {
      //Зачем? Блюрится раньше чем нажимается
      setTimeout(() => { this.isOpen = false; }, 500);
    },
    blurInput() {
      this.$emit('InputBlur');
      this.$emit('blur');
      this.close();
    },
    ...mapActions(['GET_CITY_BY_QUERY']),
  },
  computed: {},
  mounted() {
    this.load();
  },
  watch: {
    input() {
      this.search(this.input);
      this.$emit('input', this.input);
    },
    InputValue() {
      this.input = this.InputValue;
    },
  },
};
</script>

<style scoped lang="scss">
  .v-search-city {
    position: relative;
    ul {
      position: absolute;
      top: calc(100% - .5rem);
      left: 0;
      margin: 0;
      padding: 0;
      width: 100%;
      z-index: 9999;
      background: var(--background-content);
      color: var(--link);
      list-style-type: none;
      li {
        padding: .25rem 1rem;
        cursor: pointer;
        border-bottom: 1px solid var(--input-border);
        border-top: none;
      }
    }
  }
</style>
