<template>
<form id="form_share" v-show="modalOpened" v-if="currentDataset.dataset" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_share_blue.svg"> Share a copy of dataset</header>
    <p>Please enter name of the user you want to share <strong>{{ currentDataset.dataset.name }}</strong> with.</p>

    <input type="text" ref="usernameInput" name="user_name" placeholder="Enter user name" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_user_gray.svg')})`}" v-model="inputtedUsername" @keyup.enter="shareDataset">
    <a href="#" id="button_share" class="button_primary">Share dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetShareModal',
    data() {
        return {
            inputtedUsername: ''
        }
    },
    methods: {
        shareDataset: function() {
            /* #TODO */
        }
    },
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetShare
        },

        currentDataset() {
            return this.$store.state.currentDataset
        }
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.inputtedUsername = ''
            }
            else {
                this.$nextTick(() => {
                    this.$refs.usernameInput.focus()
                })
            }
        }
    }
}
</script>