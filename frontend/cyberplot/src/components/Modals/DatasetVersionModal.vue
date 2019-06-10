<template>
<form id="form_version" v-show="modalOpened" v-if="currentDataset.dataset" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_version_blue.svg"> Manage dataset versions</header>
    
    <div v-if="!currentDataset.dataset.versioningOn">
        <p>Versioning enables you to keep multiple copies of a single dataset. With the feature turned on, you will be able to switch between different versions in VR. Would you like to enable version history for <strong>{{ currentDataset.dataset.name }}</strong>?</p>
        <a @click="enableVersioning" id="button_enable" class="button_primary">Enable version history</a>
    </div>

    <div v-else-if="disableTriggered">
        <p>Disabling version history will delete all but the most recent version of <strong>{{ currentDataset.dataset.name }}</strong>. This operation cannot be reversed. If you are certain you want to continue, please type the name of your dataset into the following textbox.</p>
        
        <input type="text" ref="nameInput" name="dataset_name" :placeholder="currentDataset.dataset.name" v-model="inputtedName" @keyup.enter="disableVersioning">
        <a @click="disableVersioning" id="button_disable" :class="[nameMatches ? 'button_primary' : 'button_secondary_disabled']">Disable version history</a>
    </div>

    <div v-else>
        <p>The following are versions of <strong>{{ currentDataset.dataset.name }}</strong>.</p>
        <ul id="versions">
            <li class="version" v-for="(version, v) in currentDataset.datasetVersions" :key="version.VID">
                <img src="@/assets/images/icon_time_gray.svg"> {{ timestampToTime(version.uploadDate) }} <img src="@/assets/images/icon_rows_gray.svg"> {{ version.itemCount }} items

                <span class="actions">
                    <a @click="downloadVersion(version.VID)" id="button_download" class="interactive button_secondary"><img src="@/assets/images/icon_download_blue.svg" alt="Download version"></a>
                    <a v-if="v != 0" @click="deleteVersion(version.VID)" class="interactive button_secondary"><img src="@/assets/images/icon_delete_blue.svg" alt="Delete version"></a>
                </span>
            </li>
        </ul>

        <a @click="disableTriggered = true" id="button_disable" class="button_secondary">Disable version history</a>
    </div>
</form>
</template>

<script>
import { prettifyHumanReadableTime } from '../../utils'

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
            this.currentDataset.dataset.versioningOn = true
            this.$store.dispatch('changeCurrentDataset', true)
        },

        disableVersioning: function() {
            if(this.nameMatches) {
                this.currentDataset.dataset.versioningOn = false
                this.$store.dispatch('changeCurrentDataset')

                /* remove all versions but the last */
                let lastVersion = this.currentDataset.datasetVersions.shift()
                this.currentDataset.datasetVersions = [lastVersion]
            }
        },

        downloadVersion: function(vid) {
            this.$store.dispatch('downloadDatasetVersion', vid)
        },

        deleteVersion: function(vid) {
            this.$store.dispatch('deleteDatasetVersion', vid)
        },

        timestampToTime: function(timestamp) {
            var humanReadable = this.$moment(timestamp * 1000).tz(this.$moment.tz.guess()).calendar()
            return prettifyHumanReadableTime(humanReadable)
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
                this.inputtedName = ''
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

<style scoped>
#button_disable {
    display: block;
    margin-left: auto;

    width: intrinsic;
    width: -moz-max-content;
    width: -webkit-max-content;
}

#versions {
    padding: 0;
    margin-left: 3em;
    max-height: 13em;
    overflow-y: scroll;
    scrollbar-width: none;
    background-color: #eee;
    border-radius: 0.3em;
}

#versions li {
    padding: 0.5em;
    list-style: none;
}

.actions {
    float: right;
}

.actions a {
    margin: 0.25em;
}

.version:nth-of-type(1) #button_download {
    margin-right: 5em;
}
</style>