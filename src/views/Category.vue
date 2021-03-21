<template>
  <div class="category">
    <!--        {{PRODUCTS.paginate}}-->
    <Breadcrumbs/>

    <v-mobile-filter

    />

    <section class="category__header">
      <div class="category__header-title">
        <v-title
          :text="$route.meta.breadcrumb.label"
        />
      </div>
      <div class="category__header-count"
           v-if="PRODUCTS.paginate"
      >
        <div>Выбрано: {{PRODUCTS.paginate.count}} товара(-ов)</div>
      </div>
      <div class="category__header-filter">
        <v-btn
          BtnIcon="filter_alt"
          BtnStyle="secondary"
          BtnName="Фильтр"
          v-if="IS_MOBILE"
          v-b-toggle.mobileFilter
        />
        <v-sort-by
          v-if="SORT_TYPES.length > 0"
          :options="SORT_TYPES"
        />
      </div>
    </section>

    <section class="category__body" :class="{'mobile': IS_MOBILE}">
      <v-filter-board
        v-if="IS_DESKTOP"
      />
      <div class="category__body-list">
        <v-title
          v-if="PRODUCTS.results && !PRODUCTS.results.length"
          style="grid-column-end: none;"
          text="Товаров по данному запросу не найдено"
          type="second"
        />

        <skeleton-loading
          v-for="i in 24"
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
    <!--    v-show обязателен, так как, -->
    <!--    без него не будет обновляется номер страницы после фильтрации-->

    <vCardLine/>
  </div>
</template>

<script>
  import vCard from '@/components/app/card/v-card.vue';
  import vCardLine from '@/components/app/container/v-card-line.vue';
  import vMobileFilter from '@/components/app/mobile/slideFilter.vue';

  import {mapActions, mapGetters} from 'vuex';

  export default {
    name: 'Category',
    props: {
      slug: {
        type: String,
      },
    },
    components: {
      vCard, vCardLine, vMobileFilter,
    },
    data() {
      return {
        loading: false,
      };
    },

    methods: {
      setLoading(value) {
        this.loading = value;
      },
      setBreadCrumbs() {
        this.BREADCRUMBS({
          route: this.$route,
          breadcrumbs: this.$breadcrumbs,
        });
      },
      loadCategory() {
        this.setLoading(true);
        const data = {
          slug: this.$route.params.slug,
        };
        if (this.$route.query) {
          data.filters = this.$serialize_query(this.$route.query);
        }
        this.GET_PRODUCTS(data).then(() => {
          this.setBreadCrumbs();
        })
          .finally(() => {
            this.setLoading(false);
          });
      },

      ...mapActions(['GET_PRODUCTS', 'BREADCRUMBS']),
    },
    computed: {
      ...mapGetters(['PRODUCTS', 'SORT_TYPES', 'IS_DESKTOP', 'IS_MOBILE']),
    },

    mounted() {
      this.loadCategory();
    },
    watch: {
      '$route.params.slug'() {
        this.loadCategory();
      },
      '$route.query.page'() {
        this.loadCategory();
      },
    },
    metaInfo() {
      return {
        title: this.$route.meta.breadcrumb.label,
      };
    },

  };
</script>

<style lang="scss">

  .category {
    width: 100%;

    &__header {
      display: flex;
      justify-content: space-between;
      margin: 1rem 0;
      flex-wrap: wrap;

      > * {
        margin: .25rem 0;
      }

      &-title {
        width: 100%;
      }

      &-count {
        display: flex;
        align-items: center;
        font-size: 14px;
      }

      &-filter {
        width: 100%;
        display: flex;
        flex-wrap: wrap;

        button {
          padding: 0 !important;
        }
      }
    }

    &__body {
      margin: 1rem 0;
      display: grid;
      grid-template-columns: 300px auto;

      &.no-filter {
        display: block;
        width: 100%;
      }

      .v-filter-board {
        margin: 0 1rem 0 .25rem;
      }

      &.mobile {
        grid-template-columns: 100%;
      }

      &-list {
        display: flex;
      }
    }
  }

  .category__body-list {
    display: flex;
    flex-wrap: wrap;
    height: min-content;

    .card {
      min-width: calc(100% / 4);
      max-width: calc(100% / 4);
      flex: 1;
    }
  }

  @media (max-width: 1200px) {
    .category__body-list {
      .card {
        min-width: calc(100% / 3);
        max-width: calc(100% / 3);
      }
    }
  }

  @media (max-width: 960px) {
    .category__body-list {
      .card {
        min-width: calc(100% / 2);
        max-width: calc(100% / 2);
      }
    }
  }

  @media (max-width: 768px) {
    .category__body-list {
      .card {
        min-width: calc(100% / 2);
        max-width: calc(100% / 2);
      }
    }
  }

  @media (max-width: 360px) {
    .category__body-list {
      .card {
        min-width: calc(100% / 1);
        max-width: calc(100% / 1);
      }
    }
  }

</style>
