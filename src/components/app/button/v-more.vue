<template>
  <div class="more" v-click-outside="closeMore">
    <button
      type="button"
      class="btn more__btn"
      :class="{'active': isMore}"
      @click="openMore"
    >more_vert
    </button>
    <ul class="more__content"
        v-if="isMore"
    >
      <!--            <li><i>favorite</i>В избранное</li>-->
      <li @click="DELETE_FROM_CART({product:ProductId})"><i>delete</i>Удалить</li>
    </ul>
  </div>
</template>

<script>
  import {mapActions} from 'vuex';

  export default {
    name: 'v-more',
    props: {
      ProductId: {
        type: Number,
      },
    },
    data() {
      return {
        isMore: false,
      };
    },
    methods: {
      openMore() {
        this.isMore = true;
      },
      closeMore() {
        this.isMore = false;
      },
      ...mapActions(['DELETE_FROM_CART']),
    },
  };
</script>

<style scoped lang="scss">

  .more {
    position: relative;

    &__btn {

      &.active {
        color: var(--link-hover);
      }
    }

    &__content {
      background: var(--background-content);
      border: 1px solid var(--product-board-border);
      white-space: nowrap;
      position: absolute;
      top: 0;
      right: 0;

      padding: 0;
      margin: 0 .5rem;

      li {
        display: flex;
        align-items: center;

        i {
          font-size: 24px;
          @extend %_material-icons;
          padding: 0 .25rem;
        }

        @include link($hover: none);
        cursor: pointer;
        padding: .5rem;
      }

    }

  }

  button {
    @extend %_material-icons;
    font-size: 26px;
    color: var(--text-main);
    &:hover {
      color: var(--link-hover);
    }
  }

</style>
