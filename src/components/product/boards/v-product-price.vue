<template>
    <div class="v-product-price product__board">
        <div class="product__board__body">
            <div v-if="0" class="v-product-price__price v-product-price__price-old">
                <!--                        <span>{{product.old_price | formattedPrice}}</span>-->
                <v-currency/>
            </div>
            <div class="v-product-price__price v-product-price__price-current"
                 v-if="Product.price"
                 :class="{'disabled': !$productStatus(Product.status)}"
                 :disabled="!$productStatus(Product.status)"
            >
                <span>{{Product.price | formattedPrice}}</span>
                <v-currency/>
            </div>
        </div>
        <div class="product__board__footer" :class="{'reverse': IS_MOBILE}">
            <v-btn
                    v-if="$productStatus(Product.status)"
                    class="v-product-price__btn v-product-price__btn-buy"
                    BtnStyle="success"
                    :BtnName="CART_IDS.includes(Product.id) ? 'В корзине': 'Купить'"
                    :BtnIcon="CART_IDS.includes(Product.id) ? 'check' : ''"
                    :class="{'active': CART_IDS.includes(Product.id)}"
                    @click.native="
                            CART_IDS.includes(Product.id) ?
                            DELETE_FROM_CART({product: Product.id}) : ADD_TO_CART({product: Product.id, quantity: 1})"
            />
            <!--                Если не в наличии               -->
            <v-btn
                    v-if="!$productStatus(Product.status)"
                    BtnStyle="success"
                    class="v-product-price__btn v-product-price__btn-buy"
                    :BtnName="CART_IDS.includes(Product.id) ? 'В корзине': 'Купить'"
                    :BtnIcon="CART_IDS.includes(Product.id) ? 'check' : ''"
                    :class="{'active': CART_IDS.includes(Product.id)}"
                    :disabled="true"
            />
            <v-btn-wish
                    class="v-product-price__btn"
                    :ProductId=Product.id
            />
            <button class="btn btn-compare card-btn v-product-price__btn"></button>
        </div>
    </div>
</template>

<script>
import formattedPrice from '@/filters/formatPrice';
import vBtnWish from '@/components/app/button/v-btn-wish.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'v-product-price',
  components: {
    vBtnWish,
  },
  filters: {
    formattedPrice,
  },
  props: {
    Product: {
      // type: Object
    },
  },
  methods: {
    ...mapActions(['ADD_TO_CART', 'DELETE_FROM_CART', 'GET_CART_DETAIL']),
  },
  computed: {
    ...mapGetters(['CART_IDS', 'IS_MOBILE']),
  },
  mounted() {
    // При force reload, отображение товара в корзине
    this.GET_CART_DETAIL();
  },
};
</script>

<style scoped lang="scss">
    .v-product-price {
        display: flex;
        align-items: center;

        position: sticky;
        bottom: .25rem;

        &__price {
            padding: 0 .5rem;
            white-space: nowrap;

            &-current {
                span {
                    @include fz(24);
                }
            }

            &-old {
                @include fz(18);
                text-decoration: line-through;
                user-select: none;
                color: var(--text-second);
            }
        }

        &__btn {
            margin: .25rem .5rem;
        }

        .product__board__footer.reverse {
            width: 100%;

            .v-product-price__btn-buy {
                flex-grow: 1;
            }
        }

    }
</style>
