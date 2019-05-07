<template>
<form id="form_rename_attribute" v-show="modalOpened" v-if="currentDataset.dataset">
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename attribute</header>
    <p>Please enter a new name for <strong>{{ attributeLabel }}</strong>.</p>

    <input type="text" name="attribute_name" :placeholder="attributeLabel">
    <a href="#" id="button_rename" class="button_primary">Rename attribute</a>
</form>
</template>

<script>
export default {
    name: 'AttributeRenameModal',
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.attributeRename
        },

        selectedAttribute() {
            return this.$store.state.selectedAttribute
        },

        currentDataset() {
            return this.$store.state.currentDataset
        },

        attributeLabel() {
            return this.currentDataset.attributes[this.selectedAttribute].label 
        }
    }
}
</script>