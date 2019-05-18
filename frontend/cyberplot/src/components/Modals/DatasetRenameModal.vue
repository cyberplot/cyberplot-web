<template>
<form id="form_rename_dataset" v-show="modalOpened" v-if="currentDataset.dataset" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename dataset</header>
    <p>Please enter a new name for <strong>{{ currentDataset.dataset.name }}</strong>.</p>

    <input type="text" ref="nameInput" name="dataset_name" :placeholder="currentDataset.dataset.name" v-model="inputtedName" @keyup.enter="renameDataset">
    <a href="#" id="button_rename" class="button_primary">Rename dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetRenameModal',
    data() {
        return {
            inputtedName: ''
        }
    },
    methods: {
        renameDataset: function() {
            /* #TODO */
        }
    },
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetRename
        },

        currentDataset() {
            return this.$store.state.currentDataset
        }
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.inputtedName = ''
            }
            else {
                this.$nextTick(() => {
                    this.$refs.nameInput.focus()
                })
            }
        }
    }
}
</script>