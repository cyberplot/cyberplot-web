<template>
<form id="form_rename_dataset" v-show="modalOpened" v-if="currentDataset.dataset" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename dataset</header>
    <p>Please enter a new name for <strong>{{ currentDataset.dataset.name }}</strong>.</p>

    <input :class="{inputError: nameAlreadyUsed}" type="text" ref="nameInput" name="dataset_name" :placeholder="currentDataset.dataset.name" v-model="inputtedName" @keyup.enter="renameDataset" @keyup="checkIfNameAvailable">
    <span class="errorText" v-if="nameAlreadyUsed">Name already used.</span>
    <a @click="renameDataset" id="button_rename" class="button_primary">Rename dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetRenameModal',
    data() {
        return {
            inputtedName: '',
            nameAlreadyUsed: false
        }
    },
    methods: {
        renameDataset: function() {
            if(!this.nameAlreadyUsed) {
                this.currentDataset.dataset.name = this.inputtedName
                this.currentDataset.dataset.lastEdit = Math.floor(Date.now() / 1000)
                this.$store.dispatch('changeCurrentDataset')
            }
        },

        checkIfNameAvailable: function() {
            /* check if there is not a dataset with the same name */
            let nameAlreadyUsed = false
            this.$store.state.datasets.forEach((dataset) => {
                if(dataset.name == this.inputtedName) {
                    nameAlreadyUsed = true
                }
            })

            this.nameAlreadyUsed = nameAlreadyUsed
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