<template>
<form id="form_rename_dataset" v-show="modalOpened" v-if="currentDataset.dataset">
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename dataset</header>
    <p>Please enter a new name for <strong>{{ currentDataset.dataset.name }}</strong>.</p>

    <input type="text" name="dataset_name" :placeholder="currentDataset.dataset.name">
    <a href="#" id="button_rename" class="button_primary">Rename dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetRenameModal',
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetRename
        },

        currentDataset() {
            return this.$store.state.currentDataset
        }
    }
}
</script>