<template>
    <router-view/>
</template>

<script>
export default {
    name: 'App',
    data() {
        return {
            user: {
                id: 1,
                name: "tomires"
            }
        }
    }
}
</script>

<style>
@import './assets/stylesheets/base.css';
</style>
