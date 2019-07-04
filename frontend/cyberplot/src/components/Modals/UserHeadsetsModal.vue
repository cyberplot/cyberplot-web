<template>
<form id="form_user_headsets" v-show="modalOpened" autocomplete="off" @submit.prevent>
    <div v-if="!addingHeadset">
        <header><img src="@/assets/images/icon_vr_blue.svg"> Manage VR headsets</header>
        
        <div v-if="headsets.length == 0">
            <p>You do not currently have any VR headsets associated with your account. Would you like to add one?</p>
        </div>

        <div v-else>
            <p>The following are VR headsets associated with your account.</p>

            <ul id="headsets">
                <li class="headset" v-for="headset in headsets" :key="headset.HID">
                    <span class="metadata"><img src="@/assets/images/icon_vr_gray.svg"> <strong>{{ headset.deviceName }}</strong></span>
                    <span class="metadata"><img src="@/assets/images/icon_time_gray.svg"> {{ timestampToTime(headset.lastUsed) }}</span>

                    <span class="actions">
                        <a @click="removeHeadset(headset.HID)" class="interactive button_secondary"><img src="@/assets/images/icon_delete_blue.svg" alt="Remove headset"></a>
                    </span>
                </li>
            </ul>
        </div>

        <a @click="addingHeadset = true" id="button_enable" class="button_primary">Add VR headset</a>
    </div>

    <div v-else>
        <header><img src="@/assets/images/icon_vr_blue.svg"> Add new VR headset</header>

        <p>In order to associate a new VR headset with your account, we will use a special pairing code. Launch Cyberplot Navigator on headset you wish to add and type in the numbers that are displayed on screen.</p>
        <input :class="{inputError: codeInvalid || codeEmpty}" type="text" ref="codeInput" name="headset_code" placeholder="Pairing code" v-model="inputtedCode" @keyup.enter="addHeadset" @keydown="clearErrors">
        <span class="errorText" v-if="codeInvalid">Provided pairing code is not valid.</span>
        <span class="errorText" v-if="codeEmpty">Please enter a pairing code.</span>
        <a @click="addHeadset" id="button_enable" class="button_primary">Add VR headset</a>
    </div>
</form>
</template>

<script>
import {EventBus} from '../../utils';

export default {
    name: 'UserHeadsetsModal',
    data() {
        return {
            inputtedCode: '',
            addingHeadset: false,
            codeInvalid: false,
            codeEmpty: false
        }
    },
    methods: {
        addHeadset: function() {
            if(this.inputtedCode != '') {
                this.$store.dispatch('associateHeadsetConnector', this.inputtedCode)
            }
            else {
                this.codeEmpty = true
            }
        },

        removeHeadset: function(hid) {
            this.$store.dispatch('removeHeadsetConnector', hid)
        },

        clearErrors: function() {
            this.codeEmpty = false
            this.codeInvalid = false
        },

        timestampToTime: function(timestamp) {
            return this.$moment(timestamp * 1000).tz(this.$moment.tz.guess()).calendar()
        }
    },
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.userHeadsets
        },

        headsets() {
            return this.$store.state.headsets
        }
    },
    mounted: function() {
        EventBus.$on('successfulHeadsetAssociation', (msg) => {
            this.addingHeadset = false
            this.codeInvalid = false
            this.inputtedCode = ''
        })

        EventBus.$on('failedHeadsetAssociation', (msg) => {
            this.codeInvalid = true
        })
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.addingHeadset = false
                this.codeInvalid = false
                this.inputtedCode = ''
            }
        },
        addingHeadset: function(val) {
            if(val == true) {
                this.$nextTick(() => {
                    this.$refs.codeInput.focus()
                })
            }
        }
    }
}
</script>

<style scoped>
#headsets {
    padding: 0;
    margin-left: 3em;
    max-height: 13em;
    overflow-y: scroll;
    scrollbar-width: none;
}

#headsets li {
    padding: 0.5em;
    list-style: none;
    background-color: #eee;
    border-radius: 0.3em;
    margin-bottom: 0.5em;
}

#headsets li .metadata:not(:first-child)::before {
    content: "\a";
    white-space: pre;
}

.actions {
    float: right;
}

.actions a {
    margin-left: 0.5em;
}
</style>