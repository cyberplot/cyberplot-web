<template>
<div id="notifications" v-show="notificationsOpened">
    <img id="arrow" src="@/assets/images/popup_arrow.svg">

    <form>
        <header><img src="@/assets/images/icon_share_incoming_blue.svg"> Shared dataset</header>
        <p>
            georgecost shared <strong>Revenue Q3</strong> with you.
        </p>
    
        <a href="#" id="button_accept" class="button_primary">Accept</a>
        <a href="#" id="button_ignore" class="button_secondary">Ignore</a>
    </form>
</div>
</template>

<script>
export default {
    name: 'NotificationCenter',
    computed: {
        notificationsOpened() {
            return this.$store.state.notificationsOpened
        }
    }
}
</script>

<style scoped>
#notifications {
    position: fixed;
    right: 0;
    top: 5.9em;
    background-color: white;
    border-radius: 0.3em;
    margin-right: 2em;
    padding: 1em;
    padding-top: 0;
    box-shadow: 0 0.2em 2em 0.1em #22222233;
    width: 20em;
}

#notifications p {
    margin: 0;
    margin-bottom: 0.25em;
    padding-left: 2.75em;
}

#notifications img {
    vertical-align: middle;
    width: 2.5em;
}

#notifications header {
    font-family: 'Libre Franklin Bold';
    color: #3765ff;
    background: linear-gradient(to bottom, #64dafa, #1fbbfb 15%, #3765ff 100%);
    background-clip: border-box;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

#notifications a {
    float: right;
}

#notifications form {
    display: inline-block;
    width: 100%;
    margin-top: 1em;
}

#notifications form a:nth-of-type(2) {
    margin-right: 0.6em;
}

#notifications #arrow {
    position: fixed;
    width: 3em;
    top: 4.9em;
    right: 12.5em;
}
</style>