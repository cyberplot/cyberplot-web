<template>
<form id="form_delete" v-show="modalOpened">
    <header><img src="@/assets/images/icon_delete_blue.svg"> Delete dataset</header>
    <p>You are about to delete <strong>Iris Dataset</strong>. This operation cannot be reversed. If you are certain you want to continue, please type the name of your dataset into the following textbox.</p>

    <input type="text" name="dataset_name" placeholder="Iris Dataset">
    <a href="#" id="button_delete" class="button_primary">Delete dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetDeleteModal',
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetDelete
        }
    }
}
</script>