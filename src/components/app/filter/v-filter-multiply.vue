<template>
    <div class="v-filter-multiply">
        <label
                v-if="data"
                v-for="choice in data"
        >
            <p-check
                    class="p-default"
                    color="primary"
                    v-model="choices"
                    :value="`${choice.id}`"
            >{{choice.name}}
            </p-check>
        </label>
    </div>
</template>

<script>
    import PCheck from 'pretty-checkbox-vue/check';
    import {mapActions, mapGetters} from "vuex";
    export default {
        name: "v-filter-multiply",
        props: {
            data: {
                type: Array,
            },
            URLQuery: {
                type: String,
            },
        },
        components: {
            PCheck,
        },
        data() {
            return {
                choices: [],
            }
        },
        methods: {
            load() {
                if (this.$route.query[this.URLQuery]) {
                    this.choices = this.$route.query[this.URLQuery].split(',')
                }
                if (this.choices.length) {
                    this.change()
                }
            },
            change() {
                let data = {
                    [this.URLQuery]: this.choices.toString(),
                }
                if (data[this.URLQuery]) {
                    this.$change_query_url(data)
                } else {
                    this.$clear_query_url(this.URLQuery)
                }
                this.$submitFilters()
            },
        },
        computed: {
            ...mapGetters(['FILTERS'])
        },
        mounted() {
            this.load()
        },
        watch: {
            'choices'() {
                this.change()
            }
        }
    }
</script>

<style scoped lang="scss">
    label {
        width: 100%;
        margin: 0;
        padding: 0 .25rem;
        font-size: 14px;
        input {
            margin-right: .25rem;
        }
    }
</style>

<style lang="scss">
    .v-filter-multiply {
        * {
            max-width: 100%;
        }
        div.state{
            label{
                white-space: normal;
                text-indent: 0;
                padding-left: 1.5rem;
                &:before, &:after{
                    top: 0;
                }
            }
        }
    }
</style>
