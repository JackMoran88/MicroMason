<template>
  <div class="v-items-container">
    <div class="v-items-container__header">
      <slot name="header"></slot>
    </div>
    <div class="v-items-container__body">
      <slot name="body"></slot>
    </div>
  </div>
</template>

<script>
  export default {
    name: "v-items-container",

  }
</script>

<style scoped lang="scss">

  .v-items-container {
    display: flex;
    flex-direction: column;

    &__header{
      margin: .25rem;
    }
    &__body{
      display: flex;
      flex-wrap: wrap;
      margin-bottom: .25rem;
    }
  }

</style>
