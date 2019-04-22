<template>
<form id="form_rename_attribute" v-show="modalOpened">
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename attribute</header>
    <p>Please enter a new name for <strong>Sepal Length</strong>.</p>

    <input type="text" name="attribute_name" placeholder="Sepal Length">
    <a href="#" id="button_rename" class="button_primary">Rename attribute</a>
</form>
</template>

<script>
export default {
    name: 'AttributeRenameModal',
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.attributeRename
        }
    }
}
</script>