<template>
  <button aria-label="button" v-b-hover="isHover">{{text}}</button>
</template>

<script>
  import { VBHover } from 'bootstrap-vue'
  export default {
    name: 'v-header-wish',
    props: {
      CartCount: {
        type: Number,
      },
    },
    directives: {
      'b-hover': VBHover
    },
    data() {
      return {
        text: 'favorite_border',
        default: 'favorite_border',
        hover: 'favorite'
      }
    },
    methods: {
      isHover(value) {
        if (value) {
          this.text = this.hover
        } else {
          this.text = this.default
        }
      }
    }
  };
</script>

<style scoped lang="scss">
  button {
    @extend %_btn;
    @extend %_material-icons-outlined;
    @extend %_header-icon;
    font-weight: 100;
    position: relative;
    padding: 0;
    color: white;
    margin: .25rem;
  }
</style>
