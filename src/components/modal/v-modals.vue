<template>
  <div>

    <b-modal
      id="authModal"
      title="Вход"
      hide-footer
      centered
      scrollable
      v-if="!IS_LOGGED_IN"
    >
      <v-auth slot="default"/>
    </b-modal>

    <b-modal
      id="cartModal"
      title="Корзина"
      scrollable
      size="lg"
      hide-footer
      centered
    >
      <v-cart slot='default'/>
    </b-modal>

    <b-modal
      id="catalogModal"
      title="Каталог"

      hide-footer
      centered
    >
      <v-catalog slot="default"
                 :listCategories="CATEGORIES"
      />
    </b-modal>

    <b-modal
      id="quickViewModal"
      title="Быстрый просмотр"
      size="lg"
      hide-footer
      centered
      @hide="CLOSE_QUICK_VIEW"
    >
      <v-quick
        slot="default"
        :ProductSlug="QUICK_VIEW.ProductSlug"
      />
    </b-modal>

    <b-modal
      id="reviewAnswerModal"
      title="Отправить ответ"
      hide-footer
      centered
    >
      <v-comment-answer-form
        :ParentId="comment.answer.ParentId"
        :ProductId="comment.answer.ProductId"
      />

    </b-modal>

  </div>
</template>

<script>
  import {
    mapGetters, mapActions, mapMutations, mapState,
  } from 'vuex';
  import {eventBus} from '@/main';
  import vAuth from '@/components/app/auth/v-auth.vue';
  import vCart from '@/components/app/cart/v-cart.vue';
  import vCatalog from '@/components/app/catalog.vue';
  import vQuick from '@/components/app/card/v-quick-view.vue';
  import vCommentAnswerForm from '@/components/app/form/v-comment-answer.vue';

  export default {
    name: 'modal',
    components: {
      vAuth, vCart, vCatalog, vQuick, vCommentAnswerForm,
    },
    data() {
      return {
        comment: {
          answer: {
            ParentId: null,
            ProductId: null,
          },
        },
      };
    },
    methods: {
      load() {
        this.loadBus();
      },
      loadBus() {
        eventBus.$on('replyToComment', (data) => {
          this.comment.answer.ParentId = data.ParentId;
          if (data.ProductId.id) {
            data.ProductId = data.ProductId.id;
          }
          this.comment.answer.ProductId = data.ProductId;
          this.$bvModal.show('reviewAnswerModal');
        });
      },
      ...mapActions([
        'GET_CATEGORY_LIST', 'CLOSE_QUICK_VIEW',

      ]),
    },
    computed: {
      ...mapGetters(['CATEGORIES', 'IS_LOGGED_IN', 'LOADING']),
      ...mapGetters([
        'IS_QUICK_VIEW', 'QUICK_VIEW',

      ]),
    },
    mounted() {
      this.load();
      // this.GET_CATEGORY_LIST();
    },
    watch: {
      IS_QUICK_VIEW() {
        if (this.IS_QUICK_VIEW) {
          this.$bvModal.show('quickViewModal');
        }
      },
    },

  };
</script>

<style scoped lang="scss">

</style>

<style lang="scss">

  .modal{
    input, input:focus, input:hover, input:active {
    -webkit-box-shadow: inset 0 0 0 50px var(--modal-background) !important;
    -webkit-text-fill-color: var(--input-text) !important;
  }
  }

  button {
    &:focus {
      outline: none !important;
    }
  }

  .modal-header {
    align-items: center !important;
  }

  /*Чтобы убрать отступ слева окна*/
  .modal {
    padding: 0 !important;
    .modal-content{
      background: var(--modal-background);
    }
    .close, .close:hover{
      color: var(--modal-close) !important;
    }
    header, footer{
      border-color: var(--product-board-border);
    }
  }

  /*Чтобы не вылазоло за окно*/
  .modal-body {
    height: 100%;
    overflow: auto;

    > * {
      height: 100%;

      p, p * {
        max-width: 100%;
      }
    }

  }

  @media(min-width: 0) and (max-width: 768px) {
    .modal-dialog {
      max-width: 100% !important;
      max-height: 100% !important;
      margin: 0 !important;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      height: 100vh;
      display: flex;
      position: fixed;
      z-index: 100000;

      .modal-content {
        height: 100%;
        width: 100%;
        border-radius: 0;
      }
    }
  }

</style>
