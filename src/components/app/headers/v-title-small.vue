<template>
    <h6 class="v-title-small" :class="{
        'v-title-small__main': type === 'main',
        'v-title-small__second': type === 'second',
    }">
        {{text}}
        <slot name="default"></slot>
    </h6>
</template>

<script>
export default {
  name: 'v-title-small',
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

    .v-title-small {
        display: block;
        width: 100%;
        color: var(--text-second);
        @include fz(14px);
        font-weight: 400;
        margin: .1rem 0;

        &__main {
            @include fz(16px);
            font-weight: 500;
        }

        &__second {
            @include fz(12px);
        }
    }

    .second {
        margin: 0 .5rem;
        color: var(--text-second)
    }

</style>
