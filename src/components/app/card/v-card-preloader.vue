<template>
  <skeleton-loading class="card card-preload">
    <row class="card__image">
      <column :span="24">
        <square-skeleton
          :count="1"
        >
        </square-skeleton>
      </column>
    </row>
    <row class="card__title">
      <column :span="24">
        <square-skeleton
          :count="1"
        >
        </square-skeleton>
      </column>
    </row>
    <row class="card__reviews">
      <column :span="24">
        <square-skeleton
          :count="1"
        >
        </square-skeleton>
      </column>
    </row>
    <row class="card__price">
      <column :span="24">
        <square-skeleton
          :count="1"
        >
        </square-skeleton>
      </column>
    </row>
  </skeleton-loading>
</template>

<script>
  export default {
    name: "v-cart-preloader",
  }
</script>

<style lang="scss">

  .card-preload {
    overflow: hidden;

    .skeleton-bac-animation {
      left: 0;
      top: 0;
      z-index: 12 !important;
    }

    * {
      overflow: hidden;
    }

    .card__image {
      * {
        height: 100% !important;
      }

      padding-top: 100% !important;

      > * {
        position: absolute;
        top: 0;
      }
    }

    .card__title, .card__reviews, .card__price {
      margin-left: 0 !important;
      margin-right: 0 !important;
    }

    .card__title {
      .square, & {
        height: 32px !important;
      }
    }

    .card__reviews {
      .square, & {
        height: 24px !important;
      }
    }

    .card__price {
      .square, & {
        height: 36px !important;
      }
    }
  }

</style>
