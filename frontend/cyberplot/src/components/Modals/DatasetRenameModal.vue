<template>
<form id="form_rename_dataset" v-show="modalOpened" v-if="currentDataset.dataset" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename dataset</header>
    <p>Please enter a new name for <strong>{{ currentDataset.dataset.name }}</strong>.</p>

    <input :class="{inputError: inputError}" type="text" ref="nameInput" name="dataset_name" :placeholder="currentDataset.dataset.name" v-model="inputtedName" @keyup.enter="renameDataset" @keyup="checkIfNameAvailable">
    <span class="errorText" v-if="nameAlreadyUsed">Name already used.</span>
    <span class="errorText" v-if="nameEmpty">Name cannot be blank.</span>
    <a @click="renameDataset" id="button_rename" class="button_primary">Rename dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetRenameModal',
    data() {
        return {
            inputtedName: '',
            nameAlreadyUsed: false,
            nameEmpty: false
        }
    },
    methods: {
        renameDataset: function() {
            this.checkIfNameAvailable()
            if(!this.inputError) {
                this.currentDataset.dataset.name = this.inputtedName
                this.currentDataset.dataset.lastEdit = Math.floor(Date.now() / 1000)
                this.$store.dispatch('changeCurrentDataset')
            }
        },

        checkIfNameAvailable: function() {
            /* check if name is not blank */
            if(this.inputtedName.length == 0) {
                this.nameEmpty = true
                return
            }
            this.nameEmpty = false

            /* check if there is not a dataset with the same name */
            this.nameAlreadyUsed = false
            this.$store.state.datasets.forEach((dataset) => {
                if(dataset.name == this.inputtedName) {
                    this.nameAlreadyUsed = true
                }
            })
        }
    },
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetRename
        },

        currentDataset() {
            return this.$store.state.currentDataset
        },

        inputError() {
            return this.nameAlreadyUsed || this.nameEmpty
        }
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.inputtedName = ''
                this.nameAlreadyUsed = false
                this.nameEmpty = false
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