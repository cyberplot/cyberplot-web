<template>
<div id="notifications" v-show="notificationsOpened">
    <img id="arrow" src="@/assets/images/popup_arrow.svg">

    <span v-if="shareRequests.length === 0" id="no_notifications">No unread notifications.</span>

    <form v-for="(request, r) in shareRequests" :key="r">
        <header><img src="@/assets/images/icon_share_incoming_blue.svg"> Shared dataset</header>
        <p>
            {{ request.username }} shared <strong>{{ request.datasetName }}</strong> with you.
        </p>
    
        <a @click="acceptRequest(request)" id="button_accept" class="button_primary">Accept</a>
        <a @click="declineRequest(request)" id="button_ignore" class="button_secondary">Ignore</a>
    </form>
</div>
</template>

<script>
export default {
    name: 'NotificationCenter',
    beforeMount() {
        this.$store.dispatch('getShareRequests')
    },
    methods: {
        acceptRequest: function(request) {
            let processedRequest = request
            processedRequest.accepted = true
            this.$store.dispatch('answerShareRequest', { request: processedRequest })
        },

        declineRequest: function(request) {
            let processedRequest = request
            processedRequest.accepted = false
            this.$store.dispatch('answerShareRequest', { request: processedRequest })
        }
    },
    computed: {
        notificationsOpened() {
            return this.$store.state.notificationsOpened
        },

        shareRequests() {
            return this.$store.state.shareRequests
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
    z-index: 5;
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
    margin-top: 0.5em;
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

#no_notifications {
    text-align: center;
    display: block;
    margin-top: 1em;
    color: #777;
    font-family: 'Libre Franklin Bold';
}
</style>