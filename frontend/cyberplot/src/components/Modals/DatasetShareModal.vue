<template>
<form id="form_share" v-show="modalOpened">
    <header><img src="@/assets/images/icon_share_blue.svg"> Share a copy of dataset</header>
    <p>Please enter name of the user you want to share <strong>Iris Dataset</strong> with.</p>

    <input type="text" name="user_name" placeholder="Enter user name" class="textbox_with_icon" style="background-image: url('@/assets/images/icon_user_gray.svg');">
    <a href="#" id="button_share" class="button_primary">Share dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetShareModal',
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetShare
        }
    }
}
</script>