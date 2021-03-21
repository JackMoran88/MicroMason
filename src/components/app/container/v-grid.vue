<template>
  <div class="grid">
    <div class="grid__left" :style="left" v-if="isLeft">
      <slot name="left"></slot>
    </div>
    <div class="grid__center" :style="center" v-if="isCenter">
      <slot name="center"></slot>
    </div>
    <div class="grid__right" :style="right" v-if="isRight">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script>
  export default {
    name: "v-grid",
    props: {
      leftW: {
        type: String,
      },
      centerW: {
        type: String,
      },
      rightW: {
        type: String,
      },
      isLeft: {
        type: Boolean,
        default: false,
      },
      isCenter: {
        type: Boolean,
        default: false,
      },
      isRight: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        left: '',
        center: '',
        right: '',
      }
    },
    methods: {
      load() {
        if (this.isLeft && this.isCenter && this.isRight) {
          this.loadStyles(`width: ${this.leftW};`, `width: ${this.centerW};`, `width: ${this.rightW};`)
        } else if (!this.isLeft || !this.isRight) {
          if (!this.isLeft) {
            this.loadStyles(``, `width: calc(${this.centerW} - ${this.rightW});`, `width: ${this.rightW};`)
          }
          if (!this.isRight) {
            this.loadStyles(`width: ${this.leftW};`, `width: calc(${this.centerW} - ${this.leftW});`, `display: none;`)
          }
          if (!this.isLeft && !this.isRight) {
            this.loadStyles(``, `width: ${this.centerW}`, ``)
          }
        }
      },
      loadStyles(left, center, right) {
        this.left = left
        this.center = center
        this.right = right
      }
    },
    mounted() {
      this.load()
    },
    watch: {
      'isLeft'() {
        this.load()
      },
      'isCenter'() {
        this.load()
      },
      'isRight'() {
        this.load()
      },
    }
  }
</script>

<style scoped lang="scss">
  .grid {
    display: flex;
    width: 100%;
    &__left {

    }

    &__center {

    }

    &__right {

    }
  }
</style>
