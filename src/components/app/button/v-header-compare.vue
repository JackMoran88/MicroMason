<template>
  <button aria-label="button">compare_arrows<span v-show="CartCount >= 1">{{CartCount}}</span></button>
</template>

<script>
  export default {
    name: 'v-header-compare',
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
    @extend %_material-icons-outlined;
    @extend %_header-icon;
    font-weight: 100;
    position: relative;
    padding: 0;
    color: white;
    margin: .25rem;

    span {
      position: absolute;
      bottom: -4px;
      right: -4px;
      color: var(--accent);
      font-size: 16px;
      font-weight: bolder;
    }

  }

</style>
