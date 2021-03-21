<template>
    <h4 class="attention">{{text}}</h4>
</template>

<script>
export default {
  name: 'v-attention',
  props: {
    text: {
      type: String,
    },
  },
};
</script>

<style scoped lang="scss">

    .attention{
        display: block;
        width: 100%;
        color: var(--background-dark-second);
        @include fz(22);
        font-weight: 400;
    }

</style>
