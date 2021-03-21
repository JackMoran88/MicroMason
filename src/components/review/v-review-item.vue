<template>
    <div class="v-review-item">
        <v-comment
                :Comment=comment
        />
    </div>
</template>

<script>
import vComment from '@/components/product/tabs/components/v-comment';

export default {
  name: 'v-review-item',
  props: {
    comment: {
      type: Object,
    },
  },
  components: { vComment },
  methods: {

  },
  computed: {},
  mounted() {
  },

};
</script>

<style scoped lang="scss">

</style>
