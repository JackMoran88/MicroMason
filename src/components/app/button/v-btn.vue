<template>
  <button
    :type="BtnType"
    :disabled="BtnDisabled()"
    :class="BtnStyle"
    :aria-label="BtnAriaLabel"
  >
    <i>{{BtnIcon}}</i>{{BtnName}}
  </button>
</template>

<script>

  export default {
    name: 'v-btn',
    props: {
      BtnName: {
        type: String,
      },
      BtnType: {
        type: String,
        default: 'button',
      },
      BtnStyle: {
        type: String,
      },
      BtnIcon: {
        type: String,
        default: '',
      },
      BtnAriaLabel: {
        type: String,
        default: 'button',
      },
      BtnDisabled: {
        type: Function,
        default: () => false,
      },
    },
  };
</script>

<style scoped lang="scss">

  i {
    color: inherit;
  }

  button {
    @extend %_btn;

    display: inline-flex;
    align-items: center;
    justify-content: center;

    @include fz(14px);

    i {
      @extend %_material-icons;
      font-size: 22px;
    }
  }

  button.success {
    & {
      color: var(--button-success-text);
      background: var(--accent);
    }

    &.outline {
      color: var(--accent);
      background: transparent;
      border-color: rgba(var(--accent-hover), .6);
    }

    &.active {
      background: transparent;
      border-color: rgba(var(--accent-hover), .6);
      color: var(--accent);

      &:hover {
        color: var(--button-success-text);
        background: var(--accent);
      }
    }

    &:hover {
      color: var(--button-success-text);
      background: var(--accent-hover);
    }
  }

  button.secondary {
    @include link($hover: none, $important: false);
  }

  button.danger {
    color: #fff;
    background-color: #dc3545;
    border-color: #dc3545;

    &:hover {
      color: #fff;
      background-color: #c82333;
      border-color: #bd2130;
    }

    &:focus, &.focus {
      color: #fff;
      background-color: #c82333;
      border-color: #bd2130;
      box-shadow: 0 0 0 0.2rem rgba(225, 83, 97, 0.5);
    }
  }

  button.item {
    border: 1px solid var(--link);
    border-radius: 50px;
    font-size: 14px;
    padding: .225rem .6rem;
    margin: .25rem;
    @include link($hover: none);

    &.no-round {
      border-radius: 0;
    }

    &:hover {
      border-color: var(--link-hover);
    }
  }

  button.cart-buy {
    height: 30px !important;
    width: 30px !important;
    padding: 0 !important;
    background-size: 80% 80% !important;
    background-position: center !important;
    @extend %_material-icons-outlined;
    font-size: 28px !important;
    transition: filter .25s ease-in-out !important;
    transform: scale(-1, 1) !important;

    color: var(--card-button);

    i {
      @extend %_material-icons;
      font-size: 26px !important;
    }

    &.active {
      color: var(--accent) !important;
    }

    &:hover {
      color: var(--link-hover) !important;
    }
  }

  button.search {
    color: var(--text-light);
    text-transform: uppercase;
    @include fz(14px);
    font-weight: 500;

    i {
      @extend %_material-icons;
      font-size: 22px;
    }

    &.active {
      &:hover {
      }
    }

    &:hover {
      color: var(--accent);
    }
  }

  button.header-burger {
    padding: 0 .25rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;

    color: var(--button-burger-text);
    text-transform: uppercase;
    @include fz(14px);
    font-weight: 500;

    i {
      @extend %_material-icons;
      font-size: 37px;
    }

    &.active {
      &:hover {
      }
    }

    /*&:hover {*/
    /*  color: var(--text-muted);*/
    /*}*/
  }
</style>
