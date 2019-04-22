<template>
<div id="overlay" v-show="overlayOpened">
    <dialog>
        <a @click="closeOverlay" id="button_close" class="button_secondary"><img src="@/assets/images/icon_close_blue.svg" alt="Close dialog"></a>
        <!-- OVERLAY -->

        <UserSettingsModal />
    </dialog>
</div>
</template>

<script>
import UserSettingsModal from './Modals/UserSettingsModal.vue';

export default {
    name: 'DatasetOverlay',
    components: {
        UserSettingsModal
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