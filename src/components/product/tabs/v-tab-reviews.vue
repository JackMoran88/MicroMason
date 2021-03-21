<template>
    <section id="tab-review">
        <div class="tab-review__top-action">
            <v-btn
                    BtnName="Оставить отзыв"
                    BtnStyle="secondary"
                    v-b-modal.reviewModal
                    v-if="!$search_by(COMMENTS, 'customer', USER && USER.id)"
            />
            <v-title-small
                    v-else
                    class="mr-auto text-right"
                    text="Вы уже оставлил отзыв. Вы можете дополнить свой отзыв, ответив на него"
            />
        </div>
        <h4 v-if="!COMMENTS.length">Пока нет ни одного отзыва, вы можете стать первым!</h4>
        <v-comment
                v-else
                v-for="Comment in COMMENTS" :key="Comment.id"
                :Comment=Comment
        />

        <b-modal
                id="reviewModal"
                title="Написать отзыв"
                hide-footer
                centered
        >
            <v-comment-form
                    :ProductId="ProductId"
            />
        </b-modal>

    </section>
</template>

<script>
import vComment from '@/components/product/tabs/components/v-comment.vue';
import vCommentForm from '@/components/app/form/v-comment-form.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'v-tabs-reviews',
  components: {
    vComment, vCommentForm,
  },
  props: {
    ProductId: {
      type: Number,
    },
  },
  data() {
    return {
      author_ids: [],
      ParentId: null,
    };
  },
  methods: {
    Answer(ParentId) {
      this.ParentId = ParentId;
      this.$bvModal.show('reviewAnswerModal');
    },
    ...mapActions(['GET_COMMENTS']),
  },
  computed: {
    ...mapGetters(['COMMENTS', 'USER']),
  },
  mounted() {
    this.author_ids = [];
    this.GET_COMMENTS(this.ProductId).then(() => {
      this.COMMENTS.forEach((value) => {
        this.author_ids.push(value.customer);
      });
    });
  },
};
</script>

<style scoped lang="scss">

    .tab-review {
        &__top-action {
            display: flex;
            justify-content: flex-end;

            button {
                border: 1px solid var(--link);

                &:hover {
                    border-color: var(--link-hover);
                }
            }
        }
    }

    h4 {
        color: var(--background-dark-second);
    }

</style>
