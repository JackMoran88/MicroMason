<template>
    <h2 class="title" :class="{
        'title__main': type === 'main',
        'title__second': type === 'second',
    }">
        {{text}}
        <slot name="default"></slot>
    </h2>
</template>

<script>
export default {
  name: 'v-title',
  props: {
    text: {
      type: String,
    },
    type: {
      type: String,
    },
  },
};
</script>

<style scoped lang="scss">

    .title {
        display: block;
        width: 100%;
        color: var(--text-main);
        @include fz(26px);
        font-weight: 400;
        margin: .5rem 0;

        &__main {
            @include fz(30px);
            font-weight: 500;
        }

        &__second {
            @include fz(22px);
        }
    }

    .second {
        margin: 0 .5rem;
        color: var(--text-second)
    }

</style>
