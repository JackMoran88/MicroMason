<template>

  <div class="card" :class="{'disabled':!$productStatus(Product.status)}">
    <div class="card__image">
      <router-link
        :to="{name: 'Product', params:{
                      slug: Product.category_slug,
                      ProductSlug: Product.slug
                    }}"
      >
        <img
          v-lazy="this.$store.state.backendUrl + Product.main_image.card"
          :alt="Product.name"
          :title="Product.name"
        >
      </router-link>
    </div>
    <div class="card__title">
      <router-link
        :to="{name: 'Product', params:{slug: Product.category_slug, ProductSlug: Product.slug}}"
      >
        <div class="card__title-name" :title="Product.name">{{Product.name}}</div>
      </router-link>
    </div>
    <div class="card__reviews">
      <v-rating
        :Rating="Product.rating_avg"
        :CountReviews="Product.count_reviews"
      />
    </div>
    <div class="card__price">
      <div class="price">
        <span v-if="Product.price">{{Product.price | formattedPrice}}</span>
        <v-currency/>
      </div>
      <div class="action">
        <v-btn
          v-if="$productStatus(Product.status)"
          BtnIcon="shopping_cart"
          BtnStyle="cart-buy"
          :class="{'active': CART_IDS.includes(Product.id)}"
          @click.native="CART_IDS.includes(Product.id)?
                        DELETE_FROM_CART({product:Product.id}):
                        ADD_TO_CART({product: Product.id, quantity: 1})"
        />
      </div>
    </div>
    <div class="card__action">
      <v-btn-wish

        :ProductId="Product.id"
      />
      <v-btn-compare

        :ProductId="Product.id"
      />
      <button
        class="btn btn-quick-view card-btn"
        aria-label="button quick-view"
        @click="SHOW_QUICK_VIEW(Product.slug)"
      ></button>
    </div>

  </div>

</template>

<script>
  import vRating from '@/components/product/v-rating.vue';
  import vBtnWish from '@/components/app/button/v-btn-wish.vue';
  import vBtnCompare from '@/components/app/button/v-btn-compare.vue';
  import formattedPrice from '@/filters/formatPrice';
  import {mapActions, mapGetters} from 'vuex';

  export default {
    name: 'v-card',
    components: {
      vRating, vBtnWish, vBtnCompare,
    },
    filters: {
      formattedPrice,
    },
    props: {
      Product: {
        type: Object,
      },
    },
    methods: {
      ...mapActions(['ADD_TO_CART', 'DELETE_FROM_CART', 'GET_CART_DETAIL', 'SHOW_QUICK_VIEW']),
    },
    computed: {
      ...mapGetters(['CART_IDS']),
    },
    mounted() {

    },
  };
</script>

<style lang="scss">

  .btn-quick-view {
    @include fz(26px !important);
    transition: background-image .25s ease-in-out;

    &:after {
      content: 'visibility';
    }

    &.fill {
      color: royalblue;

      &:after {
        content: 'visibility';
        color: royalblue;
      }
    }

    &:hover {
      color: royalblue;
    }

    &:focus {
      box-shadow: none;
    }
  }


  .card {
    //@extend %_shadow;
    display: flex;
    flex-direction: column;

    z-index: 10;

    border-radius: 0;
    padding: 1rem;

    background-color: var(--card-background);
    color: var(--card-text);
    border: 1px solid var(--card-border);

    height: min-content;

    > a {
      position: absolute;

      height: 100%;
      width: 100%;

    }

    &:hover {
      z-index: 15;

      border-radius: 6px;

      transform: scale(1.05);
      transition: all 0.2s ease-in-out;
    }

    .card__image {
      display: flex;

      z-index: 11;

      height: 70%;
      max-width: 100%;
      margin: .5rem 0;
      padding-top: 100%;
      position: relative;

      a {
        display: flex;

        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;

        width: 100%;
        height: 100%;

        transition: 2s;

        img {
          max-width: 100%;
          max-height: 100%;
          margin: auto;
          padding: .5rem 0;
        }
      }
    }

    .card__title {
      z-index: 11;
      margin-bottom: 0.25rem !important;

      a {
        color: var(--card-text);

        div.card__title-name {
          display: -webkit-box;

          height: 32px;
          margin: 0 !important;

          @include fz(14px);
          line-height: 16px;
          -webkit-line-clamp: 2; /* number of lines to show */
          -webkit-box-orient: vertical;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }
    }

    .card__price {
      display: flex;
      justify-content: space-between;

      z-index: 11;

      margin: .5rem 0;

      .price {
        display: flex;
        justify-content: center;
        align-items: center;

        span {
          @include fz(24px);
        }

        .currency {
          @include fz(20px);
        }
      }

      .action {
        button {
          width: 40px;
          height: 40px;
          padding: .1rem .3rem;

          img {
            max-width: 100%;
            max-height: 100%;
          }
        }
      }
    }

    .card__reviews {
      display: flex;

      z-index: 11;

      white-space: nowrap;

      a {
        display: flex;
        justify-content: center;

        padding: 0 .2rem;
      }
    }

    .card__action {
      display: flex;
      align-items: flex-end;
      flex-direction: column;

      position: absolute;
      top: 0;
      left: 0;

      height: 100%;
      width: 100%;
      padding: .7rem;

      button {
        z-index: 12;
        margin: .2rem;
      }
    }

  }

  @media (max-width: 576px) {
    .card {
      padding: .5rem !important;

      .card__title {
        height: 28px !important;
      }

      .card__reviews {
        font-size: 12px !important;

        .star-line {
          .star {
            font-size: 14px !important;
          }
        }
      }
    }
  }


</style>
