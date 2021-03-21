<template>
  <div class="comment">
    <div class="comment__inner" :class="{'active' : USER.id && USER.id === Comment.customer}">
      <div class="comment__header">
        <span class="comment__user-name">{{Comment.author}}</span>
        <span class="comment__date">{{Comment.created_at | formattedDate}}</span>
      </div>
      <v-rating
        :Rating="Comment.star"
        :OnlyStars="true"
      />

      <div class="comment__body" v-if="Comment.text || Comment.advantages || Comment.disadvantages">
        <div class="comment__body-main">
          {{Comment.text}}
        </div>
        <div class="comment__body-advantages" v-if="Comment.advantages">
          <div class="title">Достоинства:</div>
          {{Comment.advantages}}
        </div>
        <div class="comment__body-disadvantages" v-if="Comment.disadvantages">
          <div class="title">Недостатки:</div>
          {{Comment.disadvantages}}
        </div>
      </div>
      <div class="comment__footer">
        <div class="comment__actions comment__actions__main">
          <button class="btn btn-reply" @click="ReplyToComment()">
            reply
            <span>Ответить</span>
          </button>
        </div>
        <div class="comment__actions comment__actions__sec">
<!--          <button class="btn">thumb_up_alt</button>-->
<!--          <button class="btn">thumb_down_alt</button>-->
<!--          <button class="btn">report</button>-->
          <button class="btn" @click="DeleteComment(Comment.id)"
                  v-if="USER.id && USER.id === Comment.customer">clear
          </button>
        </div>
      </div>
    </div>
    <div class="comment__outer" v-if="Comment.children"
         v-for="child in Comment.children" :key="child.id"
    >
      <div class="comment_child">
        <div class="comment__inner">
          <div class="comment__header">
            <span class="comment__user-name">{{child.author}}</span>
            <span class="comment__date">{{child.created_at | formattedDate}}
                         <button class="btn ml-auto" @click="DeleteComment(child.id)"
                                 v-if="USER.id && USER.id === child.customer">clear</button>
                        </span>
          </div>
          <div class="comment__body">
            <div class="comment__main">
              {{child.text}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import vRating from '@/components/product/v-rating.vue';
  import vInput from '@/components/app/form/v-input.vue';
  import formattedDate from '@/filters/formatDate';
  import {mapActions, mapGetters} from 'vuex';
  import {eventBus} from '@/main';

  export default {
    name: 'v-comment',
    props: {
      Comment: {
        type: Object,
      },
    },
    components: {
      vRating,
    },
    filters: {
      formattedDate,
    },
    data() {
      return {
        parentId: null,
        options: {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          timezone: 'UTC',
        },
      };
    },
    methods: {
      DeleteComment(id) {
        const data = {
          comment: id,
          product: this.Comment.product,
          author: this.USER.id,
        };
        this.DELETE_COMMENT(data);
      },
      ReplyToComment() {
        eventBus.$emit('replyToComment', {
          ParentId: this.Comment.id,
          ProductId: this.Comment.product
        });
      },
      ...mapActions(['DELETE_COMMENT']),
    },
    computed: {
      ...mapGetters(['USER']),
    },
  };
</script>

<style scoped lang="scss">

  .comment {
    &__outer {
      margin: .5rem;
      border-left: 2px dotted var(--product-board-border);

      .comment_child {
        padding-left: 1rem;

        .btn {
          @extend %_material-icons;
          padding: 0 0 0 .5rem;
        }

        .comment__body {
          border: none !important;
          padding: 1rem;
        }
      }
    }

    &__inner {
      @include def-border($color: var(--product-board-border));
      margin: .7rem 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      background: var(--comment-background);

      &.active {
        border-color: var(--comment-accent);
        border-radius: 7px;
      }

      > * {
        padding: .5rem 1rem;
      }
    }

    &__header {
      display: flex;
      justify-content: space-between;
      position: relative;
      border-bottom: 1px solid var(--product-board-border);
    }

    &__user-name, .comment__title {
      @include fz(16);
      font-weight: 500;
    }

    &__date {
      color: var(--text-second);
      @include fz(12);
    }

    &__body {
      @include fz(14);

      > * {
        .title {
          font-weight: bold;
          margin-top: .5rem;
        }
      }
    }

    &__footer {
      display: flex;
      justify-content: space-between;
      padding: .7rem 0;

      .btn {
        @include link($hover: none);
        @extend %_material-icons-outlined;
        font-size: 22px;
        @extend %_mp-0;
        margin: 0 1rem;
        display: inline-flex;
        align-items: center;

        &.active {
          @extend %_material-icons;
          font-size: 22px;
        }

        span {
          @include fz(14);
        }
      }
    }
  }

  .btn-reply {
    span {
      @extend %_font;
    }
  }

</style>
