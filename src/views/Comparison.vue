<template>
  <div class="comparison"
       :class="{'desktop': IS_DESKTOP, 'mobile': IS_MOBILE}"
  >
    <v-title
      text="Сравнение товаров"
    />
    <v-title-small
      text="Выберите категорию товаров, которых хотите сравнить"
      type="main"
      v-if="LIST.length"
    />
    <v-title-small
      text="Вы еще не добавили товары для сравнения"
      type="main"
      v-else
    />

    <div class="comparison__header"
         v-if="LIST.length"
    >
      <div class="comparison__header-categories">
        <v-btn
          v-for="category in  LIST" :key="category.id"
          :BtnName="`${category.category.name} (${category.products.length})`"
          @click.native="select(category.category.id)"
          BtnStyle="item"
        />
      </div>

      <div class="comparison__header-actions"
           v-if="CURRENT && CURRENT.length > 1"
      >
        <v-btn
          BtnName="Все"
          @click.native="all()"
          BtnStyle="item no-round"
        />
        <v-btn
          BtnName="Только различия"
          @click.native="diff()"
          BtnStyle="item no-round"
        />
      </div>
    </div>
    <div class="comparison__body table"
         v-if="CURRENT && CURRENT.length > 1"
         v-dragscroll.x="!IS_MOBILE"
    >
      <div class="product"
           v-for="item in CURRENT" :key="item.id"
           :class="{'desktop': IS_DESKTOP}"
      >
        <v-card
          :Product="item"
        />
        <div class="product-option"
             v-for="option in OPTIONS" :key="option.parameter_id"
        >
          <div class="product-option__header">{{option.parameter_name}}</div>
          <v-title-small
            :text="item.name"
            type="second"
          />
          <div class="product-option__body">
            <div class="product-option__body-item">
              {{search_option(item.id,option.parameter_id)}}
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
  import {mapActions, mapGetters} from 'vuex';
  import vCard from '@/components/app/card/v-card.vue';
  import {dragscroll} from 'vue-dragscroll';

  export default {
    name: 'Comparison',
    components: {
      vCard,
    },
    directives: {
      dragscroll,
    },
    data() {
      return {
        LIST: [],
        CURRENT: null,
        OPTIONS: null,
      };
    },
    methods: {
      load() {
        this.GET_COMPARE_DETAIL().then(() => {
          this.LIST = this.COMPARE.map((value) => ({
            category: {
              id: value.category,
              name: value.category_name,
            },
            products: [],
          }));
          this.transform();
        });
      },
      get_options() {
        if (this.CURRENT.length > 1) {
          this.OPTIONS = [];
          this.CURRENT.forEach((value) => {
            this.OPTIONS.push(...value.options);
          });
          this.OPTIONS = this.OPTIONS.filter((v, i, a) => a
            .findIndex((t) => (t.parameter_id === v.parameter_id)) === i);
          this.OPTIONS = this.OPTIONS.map((value) => ({
            parameter_name: value.parameter_name, parameter_id: value.parameter_id,
          }));
        }
      },
      transform() {
        this.LIST = this.LIST.filter((v, i, a) => a
          .findIndex((t) => (t.category.id === v.category.id)) === i);
        this.LIST.forEach((value, index) => {
          this.LIST[index].products = this.COMPARE
            .filter((obj) => (obj.category === value.category.id));
        });
      },
      select(categoryId) {
        this.CURRENT = this.LIST.filter((obj) => obj.category.id === categoryId);
        this.CURRENT = this.CURRENT.map((value) => value.products.map((item) => item.product));
        this.CURRENT = this.CURRENT[0];

        if(this.CURRENT.length > 1){
          this.get_options();
        }else{
          this.$toast('error', 'В категории лишь один товар');
        }

      },
      search_option(productId, optionId) {
        let product = this.CURRENT.filter((obj) => obj.id === productId);
        product = product[0];

        let parameter = product.options.filter((obj) => obj.parameter_id === optionId);
        if (parameter[0] && parameter[0].name != null) {
          parameter = parameter[0];
        } else {
          parameter = {name: '-'};
        }
        return `${parameter.name}`;
      },

      all() {
        this.get_options();
      },
      diff() {
        this.OPTIONS.forEach((option, index) => {
          let optionItems = [];
          this.CURRENT.forEach((item) => {
            let optionItem = item.options
              .filter((obj) => obj.parameter_id === option.parameter_id);
            optionItem = optionItem[0];
            optionItems.push(optionItem ? optionItem.name : null);
          });
          optionItems = [...new Set(optionItems)];
          if (optionItems.length <= 1) {
            this.OPTIONS.splice(index, 1);
          }
        });
      },

      ...mapActions(['GET_COMPARE_DETAIL']),
    },
    computed: {
      ...mapGetters(['COMPARE', 'COMPARE_IDS', 'IS_MOBILE', 'IS_DESKTOP']),
    },
    mounted() {
      this.load();
    },
    watch: {
      'COMPARE_IDS.length'() {
        this.load()
      },
      'COMPARE'() {
        if (this.CURRENT && this.CURRENT.length) {
          const temp = this.CURRENT[0].category_id;
          this.transform();
          this.CURRENT = null
        }
      },
    },
  };
</script>

<style scoped lang="scss">

  .comparison {
    width: 100%;

    &__header {
      margin: 1rem 0 .5rem 0;

      &-categories {
        display: flex;
        flex-wrap: wrap;

        button {
          margin: .25rem;
        }
      }

      &-actions {
        display: flex;
        margin-top: 1rem;

        button {
          border-radius: 0;
        }
      }
    }

  }

  .v-title-small__second {
    font-size: 10px;
  }

  .product.desktop {
    & {
      & {
        .product-option__header {
          opacity: 0;
        }
      }

      &:nth-child(odd) {
        .product-option__header {
          opacity: 1;
        }
      }
    }
  }

  .product {
    &-option {
      margin: 1.5rem 0;
      padding: 0 1rem;

      &__header {
        margin-bottom: .7rem;
        font-weight: bold;
        @include fz(14px)
      }

      &__body {
        font-weight: lighter;
        @include fz(16px);
      }

      &__product-name {

      }
    }
  }

  .product {
    display: grid;
    grid-template-rows: min-content;

    &-option {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
  }
</style>

<style lang="scss">
  .comparison.desktop {
    .table {
      display: grid;
      grid-auto-columns: minmax(400px, 1fr);
      grid-auto-flow: column;

      cursor: pointer;
      overflow: auto;
    }

    .card {
      display: grid;
      grid-template-columns: 25% auto 50px;
      grid-template-rows: repeat(4, min-content);

      &__image {
        grid-row: 1/span 2;

        img {
          padding: .25rem !important;
        }
      }

      &__reviews {
        display: none;
      }

      &__price {
        grid-row: 3;
        grid-column: 2/4;
        margin: .25rem 0;

        .action {
          button {
            margin: .5rem;
            padding: 0 !important;
            margin-top: 0;
            height: min-content;
            line-height: normal;
            width: 37px;
          }
        }
      }

      &__action {
        grid-column: 3;
        grid-row: 1/span 2;

        align-items: center;
        position: initial;

        padding: 0;

        > button {
          margin: .5rem;
          margin-top: 0;
          height: min-content;
          line-height: normal;
        }
      }
    }
  }

  .comparison.mobile {
    .table {
      margin: 3rem 0;
      display: grid;
      grid-auto-columns: minmax(180px, 50%);
      grid-auto-flow: column;
      overflow: auto;

    }

    .card {
      &__reviews {
        display: none;
      }

    }
  }

</style>
