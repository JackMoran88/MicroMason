<template>

  <section class="product__slider" :class="{'loading':!PAGE_LOADED, 'active': lightBoxOpened}">
    <flickity class="slider-main product__board"
              ref="flickity"
              :options="slides.length > 1 ? flickityOptionsMany : flickityOptionsOne"
    >
      <div class="carousel-cell" v-for="(slide, index) in slides" :key="slide.id"
           :data-index="index">
        <img v-lazy="slide.src" @click.exact="showImage(index)" width="720" height="720"
             :alt="Product.name">
      </div>
    </flickity>

    <flickity class="slider-nav"
              ref="flickityNav"
              :options="flickityOptionsNav" v-if="slides.length > 1"
    >
      <div class="carousel-cell" v-for="(slide, index) in slides" :key="slide.id"
           :data-index="index">
        <img v-lazy="slide.src" alt="" width="720" height="720" :alt="Product.name">
      </div>
    </flickity>

    <LightBox
      :media="slides"
      :showLightBox="false"
      ref="gallery"
      @onOpened="lightBoxOpened = true"
      @onClosed="lightBoxOpened = false"
    ></LightBox>

  </section>

</template>

<script>
import Flickity from 'vue-flickity';
import 'flickity-as-nav-for';
import LightBox from 'vue-image-lightbox';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'v-gallery',
  components: {
    Flickity, LightBox,
  },
  props: {
    slides: {
      type: Array,
    },
    Product: {
      type: Object,
    },
  },
  data() {
    return {
      flickityOptionsOne: {
        initialIndex: 0,
        pageDots: false,
        wrapAround: true,
        prevNextButtons: false,
      },

      flickityOptionsMany: {
        initialIndex: 0,
        pageDots: false,
        wrapAround: true,
        prevNextButtons: true,
      },

      flickityOptionsNav: {
        asNavFor: '.slider-main',
        contain: true,
        pageDots: false,
        prevNextButtons: false,
        freeScroll: true,
        draggable: false,
      },

      dragged: false,
      dragTimeout: null,

      lightBoxOpened: false,

    };
  },
  methods: {
    load() {
      this.GET_PRELOADER();
      this.$refs.flickity.resize();

      this.fixClickAfterDrag();
    },
    showImage(index) {
      this.$refs.gallery.showImage(index);
    },

    fixClickAfterDrag() {
      // Fix click after drag
      this.$refs.flickity.on('dragMove', function (event, pointer, moveVector) {
        this.element.classList.add('nopointer');
      });
      this.$refs.flickity.on('dragEnd', function (event, pointer) {
        this.element.classList.remove('nopointer');
      });
    },

    ...mapActions(['GET_PRELOADER']),
  },
  computed: {
    ...mapGetters(['PAGE_LOADED']),
  },
  mounted() {
    this.load();
  },
};
</script>

<style lang="scss">
  @import "~vue-image-lightbox/dist/vue-image-lightbox.min.css";

  section.product__slider {
    display: flex;
    flex-direction: row-reverse;

    position: relative;
    z-index: 40; //Если в галлерею вылазят блоки с продукта
    &.active {
      z-index: 1000;
    }

    .slider-main {
      @extend %_shadow;
      width: 100%;
      border-radius: 12px;
      border: 2px solid var(--background-light-second);
      box-sizing: content-box;

      &.nopointer {
        pointer-events: none;
      }

      .flickity-viewport {
        padding-top: 100%;
        position: relative;
        border-radius: 12px;
        height: fit-content !important;

        .flickity-slider {
          display: flex;
          position: absolute;
          top: 0;
          left: 0;
          bottom: 0;
          right: 0;
          width: 100%;
          height: 100%;

          .carousel-cell {
            width: 100%;
            height: 100%;

            img {
              width: 100%;
              height: 100%;
              object-fit: contain;
            }
          }

        }
      }

      .flickity-button {
        background: none !important;
        color: var(--background-content);
      }
    }

    .slider-nav {
      width: 80px;

      .flickity-viewport {
        height: 100% !important;
      }

      .flickity-slider {
        display: flex;
        flex-direction: column;
        transform: none !important;
        align-items: center;

        overflow-y: auto;
        overflow-x: hidden;

        @extend %_scroll-hide;

        .carousel-cell {
          position: static !important;
          border-radius: 12px;
          cursor: pointer;
          background: var(--background-light);

          width: 65px;
          height: 65px;
          min-height: 65px;
          max-height: 65px;

          img {
            //@include shadow;
            padding: .1rem;
            width: 100%;
            height: 100%;

            object-fit: contain;
            border-radius: 12px;
          }

          &.is-nav-selected {
            @extend %_shadow;

            img {
              padding: 0;
              border: 2px solid var(--accent);
            }
          }
        }
      }

    }

  }

  /*FIX LIGHT BOX*/
  .vue-lb-thumbnail-wrapper {
    width: 100%;

    .vue-lb-thumbnail {
      width: calc(100% - 100px);
      padding: 0;
      position: relative;

      button {
        position: absolute;

        &.vue-lb-thumbnail-left {
          left: -35px;
        }

        &.vue-lb-thumbnail-right {
          right: -35px;
        }
      }
    }
  }


  /* !FIX GALLERY! */

  .vue-lb-container {
    background-color: rgba(black, .9) !important;
  }

</style>
