<template>
<form id="form_rename_dataset" v-show="modalOpened">
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename dataset</header>
    <p>Please enter a new name for <strong>Iris Dataset</strong>.</p>

    <input type="text" name="dataset_name" placeholder="Iris Dataset">
    <a href="#" id="button_rename" class="button_primary">Rename dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetRenameModal',
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetRename
        }
    }
}
</script>