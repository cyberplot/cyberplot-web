<template>
<form id="form_share" v-show="modalOpened" v-if="currentDataset.dataset" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_share_blue.svg"> Share a copy of dataset</header>
    <p>Please enter name of the user you want to share <strong>{{ currentDataset.dataset.name }}</strong> with.</p>

    <input :class="{inputError: userNotSelected || requestAlreadySent}" type="text" ref="usernameInput" id="usernameInput" name="user_name" placeholder="Enter user name" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_user_gray.svg')})`}" v-model="inputtedUsername" @keyup.enter="confirmSelection" @keydown.down="selectNext" @keydown.up="selectPrevious" @keyup="getUserAutocomplete">

    <ul id="autocomplete">
        <li @click="select(u)" v-for="(user, u) in userAutocomplete" :key="user.UID" :class="{highlightedItem: (u === selectedPosition)}"><img src="@/assets/images/icon_user_blue.svg">{{ user.username }}</li>
    </ul>

    <span class="errorText" v-if="userNotSelected">Please type in a valid username.</span>
    <span class="errorText" v-if="requestAlreadySent">You have already shared the dataset with this user.</span>

    <a @click="shareDataset" id="button_share" class="button_primary">Share dataset</a>
</form>
</template>

<script>
import {EventBus} from '../../utils';

export default {
    name: 'DatasetShareModal',
    data() {
        return {
            inputtedUsername: '',
            userAutocomplete: [],
            selectedPosition: -1,
            shareInitiated: false,
            userNotSelected: false,
            requestAlreadySent: false
        }
    },
    methods: {
        shareDataset: function() {
            this.shareInitiated = true
            if(this.inputtedUsername != '') {
                this.$store.dispatch('userAutocomplete', this.inputtedUsername)
            }
        },

        completeShare: function() {
            this.shareInitiated = false

            if(this.userAutocomplete.length === 0) {
                this.userNotSelected = true
                return
            }

            this.$store.dispatch('shareCurrentDataset', this.userAutocomplete[0].uid)
            this.userAutocomplete = []
        },

        getUserAutocomplete: function(e) {
            if(e.key == 'ArrowDown' || e.key == 'ArrowUp' || e.key == 'Enter') {
                return
            }

            if(this.inputtedUsername != '') {
                this.$store.dispatch('userAutocomplete', this.inputtedUsername)
            }
            else {
                this.userAutocomplete = []
            }

            this.selectedPosition = -1
            this.userNotSelected = false
            this.requestAlreadySent = false
        },

        selectNext: function(e) {
            e.preventDefault()
            if(this.selectedPosition < this.userAutocomplete.length - 1) {
                this.selectedPosition++
            }
        },

        selectPrevious: function(e) {
            e.preventDefault()
            if(this.selectedPosition > 0) {
                this.selectedPosition--
            }
        },

        select: function(position) {
            this.selectedPosition = position
            this.confirmSelection()
        },

        confirmSelection: function() {
            if(this.selectedPosition == -1) {
                this.shareDataset()
            }
            else if(this.selectedPosition > -1 && this.selectedPosition < this.userAutocomplete.length) {
                this.inputtedUsername = this.userAutocomplete[this.selectedPosition].username
                this.userAutocomplete = []
                this.selectedPosition = -1
            }
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
    mounted: function() {
        EventBus.$on('autocomplete', (autocomplete) => {
            this.userAutocomplete = autocomplete
            if(this.userAutocomplete.length != 0) {
                this.selectedPosition = 0
            }
        })

        EventBus.$on('failedShare', (msg) => {
            this.requestAlreadySent = true
        })
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.inputtedUsername = ''
                this.selectedPosition = -1
                this.userAutocomplete = []
                this.shareInitiated = false
                this.userNotSelected = false
                this.requestAlreadySent = false
            }
            else {
                this.$nextTick(() => {
                    this.$refs.usernameInput.focus()
                })
            }
        },

        userAutocomplete: function(val) {
            if(this.shareInitiated) {
                this.completeShare()
            }
        }
    }
}
</script>

<style scoped>
#autocomplete {
    position: fixed;
    margin: 0;
    margin-left: 4em;
    background-color: #eee;
    border-radius: 0 0 0.3em 0.3em;
    list-style: none;
    padding: 0;
    width: 21em;
    box-shadow: 0 0.2em 2em 0.1em #22222233;
}

#autocomplete li {
    padding: 0.3em;
}

#autocomplete li:hover {
    background-color: #ddd;
    cursor: pointer;
    border-radius: 0 0 0.3em 0.3em;
}

#usernameInput {
    margin-bottom: 0;
}

#button_share {
    margin-top: 1em;
}

.highlightedItem {
    background-color: #ddd;
    border-radius: 0 0 0.3em 0.3em;
}

.errorText, .infoText {
    display: block;
    padding-top: 1em;
}
</style>