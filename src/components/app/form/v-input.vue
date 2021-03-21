<template>
  <label class="w-100 v-input"> {{InputTitle}}

    <skeleton-loading
      v-if="InputLoading"
    >
      <square-skeleton
        :count="1"
        :boxProperties="{height: '30px'}"
      >
      </square-skeleton>
    </skeleton-loading>


    <input
      v-show="!InputLoading"
      @input="updateInput($event.target.value)"
      class="form-control input-minimal"
      @blur="blurInput($event, InputModel)"
      @focus="focusInput($event, InputModel)"
      :type="InputType"
      :class="{'is-invalid': InputClass.invalid,'eye': InputType === 'password'}"
      tabindex="0"
      ref="form_input"
      :value="InputValue"
      :disabled="InputDisabled"

      placeholder="—"

      @keypress="InputNumberOnly ? isNumber($event): ''"

      :min="InputNumberMin ? InputNumberMin : 0"
      :max="InputNumberMax ? InputNumberMax : ''"

    >
    <span class="invalid-feedback" v-for="error in InputErrors" :key="error">
            {{error}}
        </span>

  </label>

</template>

<script>
  export default {
    name: 'v-input',
    props: {
      InputTitle: {
        type: String,
        default: 'Поле',
      },
      InputId: {
        type: String,
        default: '',
      },
      InputClass: {
        type: Object,
        default: () => ({}),
      },
      InputModel: {
        type: String,
        default: '',
      },
      InputBlur: {
        type: String,
        default: '',
      },
      InputType: {
        type: String,
        default: 'text',
      },
      InputValue: {
        // type: String,
        default: null,
      },
      InputDisabled: {
        type: Boolean,
        default: false,
      },
      InputErrors: {
        type: Array,
        default: () => [],
      },
      InputNumberOnly: {
        type: Boolean,
        default: false,
      },
      InputNumberMax: {
        type: Number,
      },
      InputNumberMin: {
        type: Number,
      },
      InputLoading: {
        type: Boolean,
        default: false,
      }
    },
    methods: {
      updateInput(value) {
        this.$emit('input', value);
      },
      blurInput(event, model) {
        this.$emit('InputBlur', {event, model});
        this.$emit('blue');
      },
      focusInput(event, model) {
        this.$emit('focus', {event, model});
      },
      isNumber(evt) {
        evt = (evt) || window.event;
        const charCode = (evt.which) ? evt.which : evt.keyCode;
        if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
          evt.preventDefault();
        } else {
          this.checkMinMax(evt);
          return true;
        }
      },
      checkMinMax(evt) {
        if (this.InputNumberMin && evt.target.value <= this.InputNumberMin) {
          evt.preventDefault();
          evt.target.value = this.InputNumberMin;
        }
        if (this.InputNumberMax && evt.target.value >= this.InputNumberMax) {
          evt.preventDefault();
          evt.target.value = this.InputNumberMax;
        }
      },

    },
  };
</script>

<style scoped lang="scss">

  label {
    @include fz(14);
    color: var(--label-text);
    width: 100%;
    margin: .5rem 0 !important;
  }

  label {
    position: relative;

    input {
      width: 100%;
    }

    button {
      width: 10%;
      position: absolute;
      top: 0;
      right: 0;

      background: none;
      border: none;

      color: #c0c0c0;
      padding: 5px;

      &.active {
        color: var(--accent);
      }

      &:focus {
        border: none;
        outline: none;
      }
    }
  }

  input, input:focus, input:hover, input:active {
    -webkit-box-shadow: inset 0 0 0 50px var(--input-background);
    -webkit-text-fill-color: var(--input-text);
  }

  input {
    border: none;
    border-bottom: 1px solid var(--input-border);
    background: var(--background-content);


    &.input-minimal {
      border: none;
      border-bottom: 1px solid var(--input-border);
      color: var(--text-dark);
      border-radius: 0;
      transition: none;

      &.is_invalid, &.is_invalid:focus {
        border-bottom: 1px solid var(--accent) !important;
      }

      &:hover {

      }

      &:focus {
        outline: none;
      }
    }

    &:focus {
      border-radius: 0;
    }
  }

  .invalid-feedback {
    display: block;
    font-size: 14px;

  }

  /*Отображать толко одну ошибку в input*/
  fieldset {
    .invalid-feedback {
      display: none;
    }

    .invalid-feedback:first-of-type {
      display: block;
    }
  }


</style>
