<template>
<form id="form_version" v-show="modalOpened" v-if="currentDataset.dataset" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_version_blue.svg"> Manage dataset versions</header>
    
    <div v-if="!currentDataset.dataset.versioningOn">
        <p>Versioning enables you to keep multiple copies of a single dataset. With the feature turned on, you will be able to switch between different versions in VR. Would you like to enable version history for <strong>{{ currentDataset.dataset.name }}</strong> ?</p>
        <a @click="enableVersioning" id="button_enable" class="button_primary">Enable version history</a>
    </div>

    <div v-else-if="disableTriggered">
        <p>Disabling version history will delete all but the most recent version of <strong>{{ currentDataset.dataset.name }}</strong>. This operation cannot be reversed. If you are certain you want to continue, please type the name of your dataset into the following textbox.</p>
        
        <input type="text" ref="nameInput" name="dataset_name" :placeholder="currentDataset.dataset.name" v-model="inputtedName" @keyup.enter="disableVersioning">
        <a @click="disableVersioning" id="button_disable" :class="[nameMatches ? 'button_primary' : 'button_secondary_disabled']">Disable version history</a>
    </div>

    <div v-else>
        <p>Versions for <strong>{{ currentDataset.dataset.name }}</strong></p>
    </div>
</form>
</template>

<script>
export default {
    name: 'DatasetVersionModal',
    data() {
        return {
            inputtedName: '',
            disableTriggered: false
        }
    },
    methods: {
        enableVersioning: function() {
            /* #TODO */
        },

        disableVersioning: function() {
            /* #TODO */
        }
    },
    computed: {
        nameMatches() {
            return this.inputtedName.toLowerCase() === this.currentDataset.dataset.name.toLowerCase()
        },

        modalOpened() {
            return this.$store.state.openedModals.datasetVersion
        },

        currentDataset() {
            return this.$store.state.currentDataset
        }
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.disableTriggered = false
            }
        },

        disableTriggered: function(val) {
            if(val == true) {
                this.$nextTick(() => {
                    this.$refs.nameInput.focus()
                })
            }
        }
    }
}
</script>

<style>
#button_disable {
    display: block;
    margin-left: auto;

    width: intrinsic;
    width: -moz-max-content;
    width: -webkit-max-content;
}
</style>