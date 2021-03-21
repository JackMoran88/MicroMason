<template>
  <span v-clipboard:copy="text" v-clipboard:success="success">
    {{text}} <i>content_copy</i>
  </span>
</template>

<script>
  export default {
    name: "v-quick-copy",
    props:{
      text:{
        type: String,
      }
    },
    methods: {
      success() {
        this.$toast('success', 'Успешно скопировано!')
      }
    },
    mounted() {
    },
  }
</script>

<style scoped lang="scss">

  span{
    cursor: pointer;
  }

  i {
      @extend %_material-icons;
      font-size: 14px;
    }

</style>
