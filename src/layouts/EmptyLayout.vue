<template>
    <div class="EmptyLayout">
        <router-view/>
    </div>
</template>

<script>
export default {
  name: 'EmptyLayout',
};
</script>

<style scoped lang="scss">
    .EmptyLayout {
        background: var(--background-content);
        min-height: 100%;
        width: 100%;
    }
</style>
