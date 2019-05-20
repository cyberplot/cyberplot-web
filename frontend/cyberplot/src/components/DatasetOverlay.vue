<template>
<div id="overlay" v-show="overlayOpened">
    <dialog>
        <a @click="closeOverlay" id="button_close" class="button_secondary"><img src="@/assets/images/icon_close_blue.svg" alt="Close dialog"></a>

        <UserSettingsModal />
        <DatasetRenameModal />
        <DatasetUpdateModal />
        <DatasetDeleteModal />
        <DatasetShareModal />
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
import AttributeRenameModal from './Modals/AttributeRenameModal.vue'

export default {
    name: 'DatasetOverlay',
    components: {
        UserSettingsModal,
        DatasetRenameModal,
        DatasetUpdateModal,
        DatasetDeleteModal,
        DatasetShareModal,
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
    }
}
</script>

<style>
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
</style>