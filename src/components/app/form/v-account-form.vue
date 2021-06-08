<template>
  <form class="account-form" :class="{'view': !change}">
    <div class="form__header">
      <slot name="header">

      </slot>
    </div>
    <div class="form__body">
      <slot name="body">

      </slot>
    </div>
    <div class="form__actions" v-if="actions">
      <slot name="actions">
        <button
          class="btn edit"
          @click="toggle"
          type="button"
        >edit
        </button>
      </slot>
    </div>
    <div class="form__footer" v-if="actions">
      <slot name="footer+"></slot>
      <slot name="footer">
        <v-btn
          :BtnIcon="IS_MOBILE ? 'clear': ''"
          :BtnName="IS_DESKTOP ? 'Отмена': ''"
          @click.native="toggle"
          BtnStyle="secondary"
        />
        <v-btn
          :BtnIcon="IS_MOBILE ? 'save': ''"
          :BtnName="IS_DESKTOP ? 'Сохранить': ''"
          @click.native="save"
          :BtnDisabled="FormSubmitDisabled"
          BtnStyle="success"
        />
      </slot>
    </div>
  </form>
</template>

<script>
  import {mapGetters} from "vuex";

  export default {
    name: 'v-account-form',
    props: {
      FormSubmitDisabled: {
        type: Function,
      },
      actions: {
        type: Boolean,
        default: true,
      },
      state: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        change: false,
      };
    },
    methods: {
      load() {
        if (this.state) {
          this.change = true;
        }
        this.toggleInputs();
      },
      toggleInputs() {
        const inputs = this.$el.querySelectorAll('input');
        if (this.change) {
          inputs.forEach((input) => {
            input.disabled = false;
          });
        } else {
          inputs.forEach((input) => {
            input.disabled = true;
          });
        }
      },
      toggle() {
        this.change = !this.change;
        this.$emit('toggle', this.change);
      },
      save() {
        this.$emit('save');
      },
    },
    computed: {
      ...mapGetters(['IS_DESKTOP', 'IS_MOBILE'])
    },
    mounted() {
      this.load();
    },
    watch: {
      change() {
        this.toggleInputs();
      },
    },
  };
</script>

<!--Поставил scoped, могут быть проблемы-->
<style lang="scss">
  form.account-form {
    @extend %_shadow;
    @include def-border;
    background: var(--account-board-bg);
    padding: 1rem;
    margin: 1.25rem 0;
    position: relative;

    fieldset {
      label {
        @include fz(12px);
        color: var(--text-second);

        input, input:focus, input:disabled, textarea {
          @include fz(14px);
          height: 30px;
          background: var(--account-board-bg);
        }

        input, input:focus, input:hover, input:active {
          -webkit-box-shadow: inset 0 0 0 50px var(--account-board-bg) !important;
          -webkit-text-fill-color: var(--input-text) !important;
        }
      }
    }

    &.view {
      label {
        color: var(--text-second);

        input, input:disabled {
          @include fz(14px);
          background: var(--account-board-bg);
          border: none;
          padding: 0;
        }
      }

      fieldset {
        span.invalid {
          display: none;
        }
      }

      .v-select {
        display: none;
      }

      .form__title {
        color: var(--text-main);
      }

      .form__footer {
        display: none;
      }
    }

    .form__header {

    }

    .form__title {
      @include fz(18px);
      margin-bottom: .5rem;
      //color: var(--text-second);
      display: inline-flex;
      align-items: center;

      span {
        @extend %_material-icons;
        font-size: 24px;
        padding-right: .5rem;
      }
    }

    .form__body {
      margin: .5rem 0;

    }

    .form__actions {
      .btn.edit {
        @include link($hover: none);
        @extend %_material-icons;
        @include fz(20px);
        //@extend %_shadow;
        position: absolute;
        top: 0;
        right: 0;
        padding: .5rem;
        background: var(--account-board-bg);
        border-radius: 0 7px 0 0;

      }
    }

    .form__footer {
      display: inline-flex;
      width: 100%;
      justify-content: flex-end;

      button {
        margin: 0 .5rem;

        height: min-content;
        align-self: center;
      }
    }

    .form__note {
      font-size: 14px;
      color: gray;
    }

  }

</style>
