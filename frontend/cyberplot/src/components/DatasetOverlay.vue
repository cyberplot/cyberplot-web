<template>
<div id="overlay" v-show="overlayOpened" @click.self="closeOverlay">
    <dialog>
        <a @click="closeOverlay" id="button_close" class="button_secondary"><img src="@/assets/images/icon_close_blue.svg" alt="Close dialog"></a>

        <UserSettingsModal />
        <DatasetRenameModal />
        <DatasetUpdateModal />
        <DatasetDeleteModal />
        <DatasetShareModal />
        <DatasetVersionModal />
        <AttributeRenameModal />
    </dialog>
</div>
</template>

<script>
import UserSettingsModal from './Modals/UserSettingsModal.vue'
import DatasetRenameModal from './Modals/DatasetRenameModal.vue'
import DatasetUpdateModal from './Modals/DatasetUpdateModal.vue'
import DatasetDeleteModal from './Modals/DatasetDeleteModal.vue'
import DatasetShareModal from './Modals/DatasetShareModal.vue'
import DatasetVersionModal from './Modals/DatasetVersionModal.vue'
import AttributeRenameModal from './Modals/AttributeRenameModal.vue'

export default {
    name: 'DatasetOverlay',
    components: {
        UserSettingsModal,
        DatasetRenameModal,
        DatasetUpdateModal,
        DatasetDeleteModal,
        DatasetShareModal,
        DatasetVersionModal,
        AttributeRenameModal
    },
    methods: {
        closeOverlay: function() {
            this.$store.commit('closeModals')
        }
    },
    computed: {
        overlayOpened() {
            return this.$store.getters.overlayOpened
        }
    },
    mounted() {
        /* close overlay when user presses escape key */
        window.addEventListener('keydown', (e) => {
            if(e.keyCode === 27) {
                this.closeOverlay()
            }
        })
    }
}
</script>

<style>
#overlay {
    background: #000000de;
    width: 100%;
    height: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 10;
}

#overlay dialog {
    width: 35em;
    background-color: #f9f9f9;
    opacity: 1;
    border-radius: 0.3em;
    padding: 1em;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: block;
    margin: 0;
    position: relative;
    border: none;
}

#overlay header {
    font-size: 1.5em;
    font-family: 'Libre Franklin Bold';
    color: #3765ff;
    background: linear-gradient(to bottom, #64dafa, #1fbbfb 15%, #3765ff 100%);
    background-clip: border-box;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

#overlay header img {
    width: 2.5em;
    vertical-align: middle;
}

#overlay p {
    margin-left: 4.1em;
    margin-top: 0;
}

#overlay form label img {
    display: block;
    width: 5em;
    margin: auto;
}

#overlay #button_close {
    float: right;
    margin: 0.5em;
    padding-left: 0.5em;
    padding-right: 0.5em;
}

#overlay #button_close img {
    width: 1.5em;
}

#overlay nav {
    display: block;
    height: 4em;
}

#overlay nav img {
    width: 4em;
}

#overlay #button_next {
    float: right;
}

#overlay #button_back {
    float: left;
}

#overlay #form_update div {
    width: 9em;
    height: 8em;
    margin: 0.75em;
    text-align: center;
    padding-top: 1.5em;
    display: inline-block;
    padding-left: 0.5em;
    padding-right: 0.5em;
}

#overlay .errorText {
    padding-left: 5em;
}

#overlay [type=text], #overlay [type=password], #overlay [type=email] {
    margin-left: 4.1em;
    width: -moz-available;
    width: -webkit-fill-available;
    width: fill-available;
}

#overlay .button_primary {
    display: block;
    margin-left: auto;

    width: intrinsic;
    width: -moz-max-content;
    width: -webkit-max-content;
}
</style>