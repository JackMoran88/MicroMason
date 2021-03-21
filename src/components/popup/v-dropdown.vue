<template>

    <div class="drop" @mouseleave="closeDropContent" v-if="data.items">
        <span class="drop__btn" @mouseover="openDropContent" @click="$router.push(data.items[0].link)">
            <i v-if="data && data.icon">{{data.icon}}</i>
            <span v-if="data">{{data.name}}</span>
        </span>
        <transition name="slideDown">
            <div class="drop__content" v-show="isOpenDropContent" v-if="data">
                <router-link
                        class="drop__item"
                        v-for="item in data.items" :key="item.link"
                        :to="item.link"
                >
                    <i class="drop__icon" v-if="item.icon">{{item.icon}}</i>
                    <span>{{item.text}}</span>
                </router-link>

                <div class="drop__item" @click="$store.dispatch('LOGOUT')" v-if="data.exit">
                    <i class="drop__icon">meeting_room</i>
                    <span>Выйти</span>
                </div>
            </div>
        </transition>
    </div>

</template>

<script>
export default {
  name: 'v-dropdown',
  props: {
    data: {
      type: Object,
    },
  },
  data() {
    return {
      isOpenDropContent: false,
    };
  },
  methods: {
    openDropContent() {
      this.isOpenDropContent = true;
    },
    closeDropContent() {
      this.isOpenDropContent = false;
    },
  },
};
</script>

<style scoped lang="scss">
    .drop {
        position: relative;
        display: inline-block;

        &__btn {
            cursor: pointer;
            display: inline-flex;
            align-items: flex-end;

            i {
                @extend %_material-icons;
                font-size: 24px;
            }
        }

        &__content {
            position: absolute;
            top: 100%;
            right: 0;
            z-index: 99;
            background-color: var(--background-light);

            display: flex;
            flex-direction: column;

            animation: .4s linksShowing;

            @include def-border();
            padding: 0;
            overflow: hidden;
        }

        &__item {
            display: inline-flex;
            align-items: center;
            padding: .3rem;
            @include fz(12);
            cursor: pointer;

            i {
                color: var(--text-main);
                @extend %_material-icons;
                font-size: 24px;
            }

            @include link(none);

            border-bottom: 1px solid var(--background-light-second);

            span {
                padding: 0 .2rem;
                display: flex;
                flex-grow: 1;
                white-space: nowrap;
                padding-right: 1.5rem;
            }

            &:hover {
                background: var(--background-light-second);
            }

            &:after {
                content: 'chevron_right';
                right: 0;

                font-family: 'Material Icons';
                font-weight: normal;
                font-style: normal;
                font-size: 24px;
                line-height: 1;
                letter-spacing: normal;
                text-transform: none;
                display: inline-block;
                white-space: nowrap;
                word-wrap: normal;
                direction: ltr;
                -webkit-font-feature-settings: 'liga';
                -webkit-font-smoothing: antialiased;
            }
        }
    }

</style>
