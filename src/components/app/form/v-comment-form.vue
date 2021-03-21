<template>

    <div class="main">
<!--        <h4>Добавить отзыв к товару</h4>-->
        <h6 v-if="!IS_LOGGED_IN">Чтобы добавить отзыв, нужно авторизироваться</h6>
        <form v-else>
            <star-rating
                    :show-rating="false"
                    @rating-selected="setRating"
                    :star-size="40"

                    :star-points="[23,2, 14,17, 0,19, 10,34, 7,50, 23,43, 38,50, 36,34, 46,19, 31,17]"
            />
            <fieldset>
                <v-input
                        InputTitle="Достоинства"
                        :InputModel="comment.advantages"
                        :InputValue="comment.advantages"
                        InputType="text"
                        v-model="comment.advantages"
                        :InputClass="{}"
                />
                <v-input
                        InputTitle="Недостатки"
                        :InputModel="comment.disadvantages"
                        :InputValue="comment.disadvantages"
                        InputType="text"
                        v-model="comment.disadvantages"
                        :InputClass="{}"
                />
                <vTextArea
                        AreaCols="5"
                        AreaTitle="Коментарий"
                        :AreaModel="comment.body"
                        :InputValue="comment.body"
                        v-model="comment.body"
                        @area="setComment"
                />
            </fieldset>

            <v-btn
                    BtnName="Оставить отзыв"
                    BtnStyle="success"
                    @click.native="SendComment"
            />
        </form>
    </div>

</template>

<script>
import {
  required, email, minLength, maxLength, sameAs, between,
} from 'vuelidate/lib/validators';
import vTextArea from '@/components/app/form/v-text-area.vue';

import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'v-comment-form',
  props: {
    ProductId: {
      type: Number,
    },
  },
  data() {
    return {
      comment: {
        advantages: null,
        body: null,
        disadvantages: null,
        rating: 0,
      },
    };
  },
  components: {
    vTextArea,
  },
  methods: {
    setRating(value) {
      this.comment.rating = value;
    },
    setComment(value) {
      this.comment.body = value;
    },

    SendComment() {
      if (this.comment.body || this.comment.advantages || this.comment.disadvantages || this.comment.rating) {
        const data = {
          product: this.ProductId,
          author: this.USER.id,
          star: this.comment.rating,
          text: this.comment.body,
          advantages: this.comment.advantages,
          disadvantages: this.comment.disadvantages,
        };
        this.SEND_COMMENT(data).then(() => {
          this.$bvModal.hide('reviewModal');
        });
      }
    },
    ...mapActions(['SEND_COMMENT']),
  },
  computed: {
    ...mapGetters(['USER', 'IS_LOGGED_IN']),
  },

};
</script>

<style scoped lang="scss">
    h6{
        color: var(--background-dark-second);
    }

    form {
        .vue-star-rating {
            margin: .25rem 0;
        }

        fieldset {
            display: flex;
            flex-direction: column;
            padding: .3rem;

            label {
                @include fz(14);
                width: 100%;
                margin: .5rem 0 !important;
            }

        }

        button {
            width: 100%;
            margin: .5rem 0;
        }
    }
</style>
