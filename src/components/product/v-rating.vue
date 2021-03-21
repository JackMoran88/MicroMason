<template>
    <div class="star-line">
        <star-rating
                :show-rating="false"
                :read-only="true"
                :round-start-rating="false"
                :rating="Rating"
                :star-size="16"

                :star-points="[23,2, 14,17, 0,19, 10,34, 7,50, 23,43, 38,50, 36,34, 46,19, 31,17]"
        />
        <a @click="onClick" v-if="!OnlyStars" class="star-line__count">{{CountReviews}} отзывов</a>
    </div>
</template>

<script>
export default {
  name: 'v-rating',
  data() {
    return {
      fill: null,
      noFill: null,
    };
  },
  props: {
    Rating: {
      type: Number,
      default: 0,
    },
    CountReviews: {
      type: Number,
      default: 0,
    },
    OnlyStars: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    onClick() {
      this.$emit('onClick', 'tab-review');
    },
  },
};
</script>

<style scoped lang="scss">

    .star-line {
        display: inline-flex;
        align-items: center;
        margin-bottom: .2rem;
        width: 100%;

        a {
            padding: 0 .3rem;
            color: var(--background-dark-second);
            font-size: 14px;
            height: 16px;
            &:hover {
                text-decoration: underline;
            }
        }
    }

</style>

<style lang="scss">

    .vue-star-rating{
        &-star{
            display: inline-flex !important;
        }
    }

</style>
