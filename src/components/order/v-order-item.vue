<template>
    <div class="v-order-item" :class="{'mobile': IS_MOBILE}">
        <img class="v-order-item__img" v-lazy="$store.state.backendUrl + product.product.main_image.cart"></img>
        <router-link
                class="v-order-item__title"
                :to="{name: 'Product', params:{slug: product.product.category_slug, ProductSlug: product.product.slug}}"
        >
            <v-title-small
                    type="second"
                    text="Название"
            />
            {{product.product.name}}
        </router-link>
        <div class="v-order-item__price">
            <v-title-small
                    type="second"
                    text="Цена"
            />
            {{product.product.price | formattedPrice}}
            <v-currency/>
        </div>
        <div class="v-order-item__quantity">
            <v-title-small
                    type="second"
                    text="Кол-во"
            />
            {{product.quantity}}
        </div>
        <div class="v-order-item__total">
            <v-title-small
                    type="second"
                    text="Сумма"
            />
            {{product.total | formattedPrice}} <v-currency/>
        </div>
    </div>
</template>

<script>
import formattedPrice from '@/filters/formatPrice';
import { mapGetters } from 'vuex';

export default {
  name: 'v-order-item',
  props: {
    product: {
      type: Object,
    },
  },
  filters: {
    formattedPrice,
  },

  computed: {
    ...mapGetters(['IS_DESKTOP', 'IS_MOBILE']),
  },
};
</script>

<style scoped lang="scss">

    .currency{
        font-size: 14px;
        margin: 0;
    }

    .v-order-item {
        display: grid;
        grid-template-columns: 56px 3fr repeat(3, min-content);
        margin: .5rem 0;
        &.mobile{
            grid-template-columns: 56px 3fr repeat(2, min-content);
            > *:nth-child(3){
                display: none;
            }
            > * {
                margin: .25rem 0;
            }
        }

        > * {
            padding: 0 .25rem;
        }

        &__img {
            width: 95%;
            max-width: 95%;
            object-fit: contain;
        }

        &__title {
            font-size: 14px;
            overflow: hidden;
            color: var(--link);
        }

        &__price, &__quantity, &__total{
            text-align: center;
            white-space: nowrap;
            font-size: 14px;
        }

        &__price {

        }

        &__quantity {

        }

        &__total {

        }

    }

</style>
