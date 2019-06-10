<template>
<form id="form_delete" v-show="modalOpened" v-if="currentDataset.dataset" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_delete_blue.svg"> Delete dataset</header>
    <p>You are about to delete <strong>{{ currentDataset.dataset.name }}</strong>. This operation cannot be reversed. If you are certain you want to continue, please type the name of your dataset into the following textbox.</p>

    <input type="text" ref="nameInput" name="dataset_name" :placeholder="currentDataset.dataset.name" v-model="inputtedName" @keyup.enter="deleteDataset">
    <a @click="deleteDataset" id="button_delete" :class="[nameMatches ? 'button_primary' : 'button_secondary_disabled']">Delete dataset</a>
</form>
</template>

<script>
export default {
    name: 'DatasetDeleteModal',
    data() {
        return {
            inputtedName: ''
        }
    },
    methods: {
        deleteDataset: function() {
            if(this.nameMatches) {
                this.$store.dispatch('deleteCurrentDataset')
            }
        }
    },
    computed: {
        nameMatches() {
            return this.inputtedName.toLowerCase() === this.currentDataset.dataset.name.toLowerCase()
        },

        modalOpened() {
            return this.$store.state.openedModals.datasetDelete
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

<style scoped>
#button_delete {
    display: block;
    margin-left: auto;

    width: intrinsic;
    width: -moz-max-content;
    width: -webkit-max-content;
}
</style>