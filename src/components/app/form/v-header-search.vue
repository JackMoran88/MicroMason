<template>
  <form
    class="form-search form-inline"
    v-on:submit.prevent="search"
    v-click-outside="clear"
    :class="{'focus': isList, 'mobile': IS_MOBILE}"
  >
    <div class="form-search__body">
      <input
        class="form-control"
        type="text"
        placeholder="Поиск"
        aria-label="Поиск"
        v-model="input"
        @input="dynamic"
        @click="dynamic"
        @blur="setIsList(false)"
        @focus="setIsList(true)"
        ref="input"
      >
      <v-btn
        BtnIcon="close"
        v-if="IS_MOBILE && isList"
        @click.native="close()"
        style="z-index: 2"
      />
      <v-btn
        BtnIcon="search"
        BtnStyle="search"
        BtnType="submit"
      />
    </div>
    <div class="form-search__content" v-if="isList">
      <div
        class="form-search__content-item"
        v-for="item in PRODUCT_SEARCH_LIST"
      >
        <router-link
          :to="{name: 'Product', params:{slug: item.category_slug, ProductSlug: item.slug}}"
        >{{item.name}}
        </router-link>
      </div>

      <div
        class="form-search__content-item form-search__content-item__category"
        v-for="item in CATEGORY_SEARCH_LIST"
      >
        <router-link
          :to="{name: 'Category', params:{slug: item.slug}}"
        >Категория: {{item.name}}
        </router-link>
      </div>
    </div>
  </form>
</template>

<script>
  import {mapActions, mapGetters, mapMutations} from 'vuex';

  export default {
    name: 'v-header-search',
    props: {},
    data() {
      return {
        input: '',
        isList: false,
      };
    },
    methods: {
      setIsList(value) {
        //Не успевают отрабатывать нажатия на моб
        setTimeout(()=>{
          this.isList = value
        },100)
      },
      search() {
        if (this.input.length >= 1) {
          if (this.$route.query.text !== this.input) {
            for (const category of this.CATEGORY_SEARCH_LIST) {
              if (category.name.toLowerCase() === this.input.toLowerCase()) {
                this.$router.replace({
                  name: 'Category', params: {slug: category.slug},
                });
                return 1;
              }
            }

            this.$router.replace({
              name: 'Search',
              query: {
                text: this.input.trim(),
              },
            });
          }
        }
      },
      dynamic() {
        //Для мобильных девайсов, v-model не воспринимает ввод
        this.input = this.$refs.input.value

        if (this.input.length < 2) {
          this.clear();
        }
        if (this.input.length > 2) {
          this.GET_PRODUCT_BY_SEARCH_LIST({query: this.input.trim()});
          this.GET_CATEGORY_BY_SEARCH_LIST({query: this.input.trim()});
        }
      },
      clear() {
        if (this.PRODUCT_SEARCH_LIST.length || this.CATEGORY_SEARCH_LIST.length) {
          this.CLEAR_PRODUCT_SEARCH_LIST();
          this.CLEAR_CATEGORY_SEARCH_LIST();
        }
      },
      close() {
        this.input = ''
        this.clear()
      },
      ...mapActions(['GET_PRODUCT_BY_SEARCH_LIST', 'GET_CATEGORY_BY_SEARCH_LIST']),
      ...mapMutations(['CLEAR_PRODUCT_SEARCH_LIST', 'CLEAR_CATEGORY_SEARCH_LIST']),
    },
    computed: {
      ...mapGetters(['PRODUCT_SEARCH_LIST', 'CATEGORY_SEARCH_LIST', 'IS_MOBILE']),
    },
    watch: {
      $route() {
        this.input = '';
        this.$refs.input.blur()
        this.clear();
      },
    },
  };
</script>

<style scoped lang="scss">

  .form-search {
    padding: 0;
    border: none;
    position: relative;

    &__body {
      display: flex;
      flex-wrap: nowrap;
      background: var(--background-dark-accent);
      border-radius: .25rem;
      flex-grow: 1;
    }


    input[type='text'] {
      background: var(--background-dark-accent);
      border-color: var(--background-dark-accent);
      color: white;
      margin: 0 !important;
      width: 100%;
    }

    button {
      color: var(--text-light);
    }

    &__content {
      z-index: 20;
      position: absolute;
      width: 100%;
      top: 100%;
      left: 0;

      &-item {
        background: var(--background-dark-accent);
        padding: .5rem .7rem;
        white-space: nowrap;
        overflow: hidden;

        a {
          @include link($color: white);
          @include fz(14px);
        }

        &__category {
          a {
            @include link($color: var(--accent));
          }
        }
      }
    }


    &.mobile.focus {
      background: var(--background-dark);
      left: 0;
      right: 0;
      position: absolute;
      z-index: 1;
      margin: auto 0;
      height: 100%;

      input, .form-search__body {
        width: 100%;
        border-radius: 0;
      }
    }
  }

</style>

<!--<form class="form-search form-inline mt-0 mt-md-0 mx-auto col-6 row d-lg-flex d-md-none d-sm-none d-none">-->
<!--<form class="form-search form-inline mt-0 mt-md-0 mx-auto col-8 row d-sm-flex d-lg-none">-->
