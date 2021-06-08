<template>
    <div class="main">
        <h6 v-if="!IS_LOGGED_IN">Чтобы ответить, нужно авторизироваться</h6>
        <form v-else>
            <fieldset>
                <vTextArea
                        AreaCols="5"
                        AreaTitle="Коментарий"
                        :AreaModel="answer.body"
                        :InputValue="answer.body"
                        v-model="answer.body"
                        @area="setAnswer"
                />
            </fieldset>

            <v-btn
                    BtnName="Оставить отзыв"
                    @click.native="SendAnswer"
                    BtnStyle="success"
            />
        </form>
    </div>
</template>

<script>

import vTextArea from '@/components/app/form/v-text-area';

import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'v-comment-answer',
  props: {
    ParentId: {
      type: Number,
    },
    ProductId: {
      type: Number,
    },
  },
  data() {
    return {
      answer: {
        body: null,
      },
    };
  },
  components: {
    vTextArea,
  },
  methods: {
    setAnswer(value) {
      this.answer.body = value;
    },
    SendAnswer() {
      if (this.answer.body) {
        const data = {
          parent: this.ParentId,
          product: this.ProductId,
          author: this.USER.id,
          text: this.answer.body,
        };
        this.SEND_ANSWER(data).then(() => {
          this.$bvModal.hide('reviewAnswerModal');
        });
      }
    },
    ...mapActions(['SEND_COMMENT', 'SEND_ANSWER']),
  },
  computed: {
    ...mapGetters(['USER', 'IS_LOGGED_IN']),
  },
};
</script>

<style scoped lang="scss">

    h6 {
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
                @include fz(14px);
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
