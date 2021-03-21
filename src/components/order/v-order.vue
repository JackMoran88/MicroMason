<template>
  <div class="v-order">
    <div class="v-order__container">
      <div class="v-order__header" @click="toggleBody" :class="{'mobile':IS_MOBILE}">
        <div
          v-if="order && order.status"
          class="v-order__header-status"
          :class="'status-'+order.status.order_by"

        >
          <p>№ {{order.id}} от {{order.created_at | formattedDate}}</p>
          <p>{{order.status.name}}</p>
        </div>
        <div class="v-order__header-price" v-if="!body">
          <p>Сумма заказа</p>
          <p>{{order.total | formattedPrice}}
            <v-currency/>
          </p>
        </div>
        <div class="v-order__header-goods" v-if="!body && IS_DESKTOP">
          <img
            v-for="product in order.order_products"
            v-lazy="$store.state.backendUrl +  product.product.main_image.cart"
            alt=""
          >
        </div>
        <v-btn
          BtnStyle="secondary"
          class="v-order__header-toggle"
          :BtnIcon="body ? 'keyboard_arrow_up': 'keyboard_arrow_down'"
        />
      </div>
      <transition name="fade">
        <div class="v-order__body" :class="{'mobile':IS_MOBILE}" v-if="body">
          <div class="v-order__body-shipping-info">
            <v-title-small
              text="Информация о заказе"
            />
            <div v-if="order.address && order.shipping">
              <div class="v-order__body-shipping-info-item">
                <span>{{order.address.first_name}} {{order.address.last_name}}</span>
              </div>
              <div class="v-order__body-shipping-info-item">
                <span>{{order.address.email}}</span>
              </div>
              <div class="v-order__body-shipping-info-item">
                <span>{{order.address.postalCode}}</span>
              </div>
              <div class="v-order__body-shipping-info-item">
                <span>{{order.address.phone_number}}</span>
              </div>
              <div class="v-order__body-shipping-info-item">
                <span>{{order.address.city}}</span>
              </div>
              <div class="v-order__body-shipping-info-item">
                <span>{{order.shipping.name}}</span>
              </div>
            </div>

            <div v-if="order.delivery.length">
              <div class="v-order__body-shipping-info-item">
                <v-quick-copy :text="order.delivery[0].int_doc_number"/>
              </div>
              <div class="v-order__body-shipping-info-item">
                <span>{{order.delivery[0].status}}</span>
              </div>
            </div>

          </div>
          <div class="v-order__body-goods">
            <v-title-small
              text="Товары"
            />
            <v-order-item
              v-if="order"
              v-for="product in order.order_products"
              :key="product.id"
              :product="product"
            />
          </div>
          <div class="v-order__body-payment-info">
            <v-title-small
              text="Информация об оплате"
            />
            <div>
              <div class="v-order__body-payment-info-item">
                <span>Оплата</span>
                <span>{{order.payment_method.name}}</span>
              </div>
              <div class="v-order__body-payment-info-item">
                <span>Статус</span>
                <span>{{order.paid}}</span>
              </div>
              <div class="v-order__body-payment-info-item">
                <span>Доставка</span>
                <span>{{order.shipping.price | formattedPrice}} <v-currency/></span>
              </div>
              <div class="v-order__body-payment-info-item">
                <span>Итого</span>
                <span>{{order.total + order.shipping.price | formattedPrice}} <v-currency/></span>
              </div>
              <div class="v-order__body-payment" v-if="parseInt(order.paid_status) === 0">
                <v-liq-pay
                  :order_id="order.id"
                  class="w-100"
                />
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
  import vOrderItem from '@/components/order/v-order-item';
  import {dragscroll} from 'vue-dragscroll';
  import formattedPrice from '@/filters/formatPrice';
  import formattedDate from '@/filters/formatDate';
  import {mapGetters} from 'vuex';

  export default {
    name: 'v-order',
    components: {
      vOrderItem,
    },
    filters: {
      formattedPrice, formattedDate,
    },
    props: {
      order: {
        type: Object,
      },
    },
    directives: {
      dragscroll,
    },
    data: () => ({
      body: false,
      orderData: {
        fullPrice: 0,
      },
    }),
    methods: {
      toggleBody() {
        this.body = !this.body;
      },
    },
    computed: {
      ...mapGetters(['IS_DESKTOP', 'IS_MOBILE']),
    },
  };
</script>

<style scoped lang="scss">

  .v-order {
    width: 100%;
    font-size: 14px;

    &__container {
      @include def-border();
      @extend %_shadow;
      width: 100%;
      padding: 1rem;
      background: var(--background-content);
    }

    &__header {
      min-height: 40px;
      display: grid;
      grid-template-columns: 40% 30% auto 40px;

      &.mobile {
        grid-template-columns: 60% 30% auto 40px;
      }

      &-status, &-price {
        p:first-child {
          font-size: 12px;
          color: var(--text-second);
        }

        p {
          margin: 0;
          font-size: 14px;
        }
      }

      &-status {
        padding-left: 12px;
        position: relative;

        &:before {
          display: block;
          position: absolute;
          border-radius: 12px;
          overflow: hidden;
          top: 0;
          left: 0;
          content: '';
          height: 100%;
          width: 4px;
          background: var(--text-second);
        }

        &.status {
          &-0:before {
            background: gray;
          }

          &-1:before {
            background: coral;
          }

          &-2:before {
            background: aquamarine;
          }

          &-3:before {
            background: lightskyblue;
          }

          &-4:before {
            background: cornflowerblue;
          }

          &-5:before {
            background: green;
          }
        }

        &.close {
          &:before {
            background: red;
          }
        }
      }

      &-goods {
        height: 100%;
        max-height: 100%;
        display: flex;
        justify-content: flex-end;

        img {
          max-height: 40px;
          max-width: 40px;
          object-fit: contain;
        }
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
      display: grid;
      grid-template-columns: 35% 65%;
      margin: .5rem 0;

      width: 100%;

      &.mobile {
        grid-template-columns: 100%;
        grid-template-rows: repeat(3, min-content);

        .v-order__body-payment-info {
          grid-column: 1;
        }
      }

      &-shipping-info {
        font-size: 12px;

        &-item {
          margin: .5rem 0;
        }
      }

      &-payment-info {
        grid-column: 2;

        &-item {
          display: flex;
          justify-content: space-between;

          width: 100%;

          span {
            margin: .25rem 0;
            font-weight: 300;
          }
        }
      }
    }
  }

</style>
