<template>
  <transition name="zoom">
    <v-btn
      BtnStyle="secondary"
      class="v-back-to-top"
      BtnIcon="keyboard_arrow_up"
      v-show="isVisible"
      @click.native="backToTop"
    />
  </transition>
</template>

<script>
  export default {
    name: 'v-back-to-top',
    data() {
      return {
        isVisible: false,
      };
    },
    methods: {
      initToTopButton() {
        window.addEventListener('scroll', () => {
          this.isVisible = document.documentElement.scrollTop > 500;
        });
      },
      backToTop() {
        this.$scrollToTop();
      },
    },
    mounted() {
      this.initToTopButton();
    },
  };
</script>

<style lang="scss">
  button.v-back-to-top {
    border-radius: 5px;
    color: var(--link-hover);
    //background-color: rgba($bg_dark, .8);
    position: fixed;
    width: 45px;
    height: 45px;
    right: 15px;
    bottom: 15px;

    display: flex;
    align-items: center;
    justify-content: center;

    z-index: 99;

    i {
      font-size: 48px;
    }
  }

</style>
