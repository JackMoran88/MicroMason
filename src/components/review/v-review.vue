<template>
    <div class="v-review" v-if="review && review.product && review.product.main_image">
        <div class="v-review__container">
            <div class="v-review__header" @click="toggleBody" :class="{'mobile':IS_MOBILE}">
                <div class="v-review__header-img">
                    <img v-lazy="this.$store.state.backendUrl + review.product.main_image.cart">
                </div>
                <div class="v-review__header-title">
                    <router-link
                            :to="{name: 'Product', params:
                            {slug: review.product.category_slug, ProductSlug: review.product.slug}}"
                    >
                        {{review.product.name}}
                    </router-link>
                </div>
                <div class="v-review__header-star">
                    <v-rating
                            :Rating="review.star"
                            :OnlyStars="true"
                    />
                </div>
                <v-btn
                        BtnStyle="secondary"
                        class="v-review__header-toggle"
                        :BtnIcon="body ? 'keyboard_arrow_up': 'keyboard_arrow_down'"
                />
            </div>
            <transition name="fade">
                <div class="v-review__body" :class="{'mobile':IS_MOBILE}" v-if="body">
                    <v-review-item
                            :comment="review"
                    />
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import vReviewItem from '@/../src/components/review/v-review-item';
import vRating from '@/components/product/v-rating';

export default {
  name: 'v-review',
  components: {
    vReviewItem, vRating,
  },
  props: {
    review: {
      type: Object,
    },
  },
  data: () => ({
    body: false,
  }),
  methods: {
    toggleBody() {
      this.body = !this.body;
    },
    getProduct() {
      if (this.review.product && !this.review.product.id) {
        this.GET_PRODUCTS_BY_IDS([this.review.product]).then((data) => {
          this.review.product = data[0];
        });
      }
    },

    ...mapActions(['GET_PRODUCTS_BY_IDS']),
  },
  computed: {
    ...mapGetters(['IS_DESKTOP', 'IS_MOBILE']),
  },
  mounted() {
    this.getProduct();
  },
  watch: {
    review() {
      this.getProduct();
    },
  },
};
</script>

<style scoped lang="scss">

    .v-review {
        width: 100%;
        font-size: 14px;

        &__container {
            @include def-border();
            @extend %_shadow;
            width: 100%;
            padding: .5rem;
            background: var(--background-light);
        }

        &__header {
            min-height: 40px;
            display: grid;
            grid-template-columns: 48px auto 100px 40px;

            &.mobile {
                grid-template-columns: 48px auto 100px 40px;
            }

            &-img {
                height: 100%;
                max-height: 100%;
                display: flex;
                justify-content: center;

                img {
                    max-height: 40px;
                    max-width: 40px;
                    object-fit: contain;
                }
            }

            &-title {
                display: flex;
                align-items: center;
                padding: 0 .5rem;

                a {
                    @include link;
                }
            }
            &-star{
                display: flex;
                align-items: center;
            }

            &-toggle {
                width: 40px;
                font-size: 26px;
                height: 40px;
                padding: .25rem .5rem;
                grid-column: 4;
            }

        }

        &__body {
            margin: .5rem 0;
            width: 100%;

        }
    }

</style>
