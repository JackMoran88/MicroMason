<template>
  <div class="category">
    <Breadcrumbs/>
    <section class="category__header">
      <div class="category__header-title">
        <v-title
          :text="$route.meta.breadcrumb.label"
        />
      </div>

      <v-items-container>
        <div slot="header">
          <v-title-small
            text="Возможно вы искали категорию"
          />
        </div>
        <div slot="body">
          <router-link
            v-for="category in  categories" :key="category.id"
            :to="{name: 'Category', params:{slug: category.slug}}"
          >
            <v-btn
              :BtnName="`${category.name}`"
              BtnStyle="item"
            />
          </router-link>
        </div>
      </v-items-container>
      <div class="category__header-filter">
        <v-sort-by
          v-if="SORT_TYPES && PRODUCTS.results && SORT_TYPES.length > 0 && PRODUCTS.results.length"
          :options="SORT_TYPES"
          @selected="sort"
          :Current="sort_by"
        />
      </div>
    </section>

    <section class="category__body no-filter" :class="{'mobile': IS_MOBILE}">
      <v-filter-board
        v-if="IS_DESKTOP"
        :onlyPrice="true"
      />
      <div class="category__body-list">
        <v-title
          v-if="PRODUCTS.results && !PRODUCTS.results.length"
          style="grid-column-end: none;"
          text="Товаров по данному запросу не найдено"
          type="second"
        />

        <skeleton-loading
          v-for="i in 24" :key="i"
          class="card card-preload"
          v-if="loading"
        >
          <row class="card__image">
            <column :span="24">
              <square-skeleton
                :count="1"
              >
              </square-skeleton>
            </column>
          </row>
          <row class="card__title">
            <column :span="24">
              <square-skeleton
                :count="1"
              >
              </square-skeleton>
            </column>
          </row>
          <row class="card__reviews">
            <column :span="24">
              <square-skeleton
                :count="1"
              >
              </square-skeleton>
            </column>
          </row>
          <row class="card__price">
            <column :span="24">
              <square-skeleton
                :count="1"
              >
              </square-skeleton>
            </column>
          </row>
        </skeleton-loading>

        <v-card
          v-for="product in PRODUCTS.results" :key="product.id"
          :Product="product"
        />

        <v-paginate
          style="grid-column: 1/end"
          v-if="PRODUCTS.paginate"
          v-show="PRODUCTS.paginate.count_page > 1"
          :PageCount="PRODUCTS.paginate.count_page"
          :Link="PRODUCTS.paginate.links.next || PRODUCTS.paginate.links.previous"
          :Current="PRODUCTS.paginate.current_page"
        />
      </div>
    </section>
    <router-view></router-view>
  </div>
</template>

<script>
  import vCard from '@/components/app/card/v-card.vue';

  import {mapActions, mapGetters} from 'vuex';

  export default {
    name: 'Search',
    data() {
      return {
        isQuickView: false,
        QuickViewSlug: null,
        sort_by: null,
        data: {
          slug: this.slug,
          sort_by: this.sort_by,
        },
        loading: false,

        categories: null,
      };
    },
    components: {
      vCard,
    },
    methods: {
      setLoading(value) {
        this.loading = value;
      },
      setSortBy(value = this.$route.query.sort) {
        this.sort_by = parseInt(value, 10);
      },
      setBreadCrumbs() {
        this.BREADCRUMBS({
          route: this.$route,
          breadcrumbs: this.$breadcrumbs,
        });
        this.$route.meta.breadcrumb.label = `Поиск по запросу: "${this.$route.query.text}"`;
        this.UPDATE_BREADCRUMBS({route: this.$route});
      },
      loadSearch() {
        if (this.$route.query.text) {
          this.setLoading(true)
          this.setSortBy();
          const data = {
            query: this.$route.query.text,
          };
          if (this.$route.query.sort) {
            data.sort_by = this.$route.query.sort;
          }
          if (this.$route.query.page) {
            data.page = this.$route.query.page;
          }

          this.GET_CATEGORY_BY_SEARCH_LIST({query: this.$route.query.text}).then((data) => {
            this.categories = data.data
          })

          this.GET_PRODUCT_BY_SEARCH(data).then(() => {
            this.setBreadCrumbs();
            this.setLoading(false)
          });
        }
      },
      sort(value) {
        this.sort_by = value;
        this.loadSearch();
      },

      ...mapActions(['BREADCRUMBS', 'UPDATE_BREADCRUMBS', 'GET_PRODUCT_BY_SEARCH', 'GET_CATEGORY_BY_SEARCH_LIST']),
    },
    computed: {
      ...mapGetters(['PRODUCTS', 'SORT_TYPES', 'IS_MOBILE', 'IS_DESKTOP']),
    },

    mounted() {
      this.loadSearch();
    },
    watch: {
      '$route.query.text'() {
        this.loadSearch();
      },
      '$route.params.slug'() {
        this.loadSearch();
      },
      '$route.query.page'() {
        this.loadSearch();
      },

    },

  };
</script>

<style scoped lang="scss">

  .filter-board {
    display: flex;
    justify-content: flex-end;
  }

</style>
