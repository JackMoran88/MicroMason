<template>
    <form class="form" ref="form">
        <slot name="header"></slot>
        <slot name="body"></slot>
        <slot name="errors"></slot>
        <slot name="footer"></slot>
    </form>
</template>

<script>
export default {
  name: 'v-form',
  methods:{
    reset(){
      this.$refs.form.reset()
    },
  }

};
</script>

<style scoped lang="scss">

    form.type-1 {
        padding: .5rem;
    }

    form {
        label {
            cursor: pointer;
        }

        fieldset {
            display: flex;
            flex-direction: column;
            padding: .3rem;

            label {
                @include fz(14px);
                color: var(--label-text);
                margin: 0;
                width: 100%;
            }

            input {
                width: 100%;
            }
        }
    }

    .form{
        &__header{
            text-transform: uppercase;
        }
        &__errors{
            color: red;
            > * {
                font-size: 14px;
                width: 100%;
                margin: .25rem 0;
            }
        }
    }

</style>
