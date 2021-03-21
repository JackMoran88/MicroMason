<template>
    <button></button>
</template>

<script>
export default {
  name: 'v-header-wish',
  props: {
    CartCount: {
      type: Number,
    },
  },
};
</script>

<style scoped lang="scss">
    button {
        @extend %_btn;
        @extend %_header-icon;
        font-weight: 100;
        position: relative;
        padding: 0;
        margin: .25rem;

        &:after{
            content:'favorite_border'
        }
        &:hover {
            &:after{
                content:'favorite'
            }
        }

    }
</style>
