<template>
<section id="content" v-if="currentDataset.dataset">
    <div id="dataset_panel">
        <h2>{{ currentDataset.dataset.name }}</h2>
        <div id="dataset_menu">
            <ul id="dataset_details">
                <li><img src="@/assets/images/icon_rows_gray.svg"> {{ currentDataset.dataset.itemCount }} items</li>
                <li><img src="@/assets/images/icon_attribute_gray.svg"> {{ currentDataset.attributes.length }} attributes</li>
                <li><img src="@/assets/images/icon_time_gray.svg"> Edited {{ lastEdit }}</li>
            </ul>

            <ul id="dataset_actions">
                <a @click="showDatasetUpdateModal" class="interactive button_secondary"><li><img src="@/assets/images/icon_update_blue.svg" alt="Update dataset"></li></a>
                <a @click="showDatasetVersionModal" class="interactive button_secondary"><li><img src="@/assets/images/icon_version_blue.svg" alt="Version history"></li></a>
                <a @click="downloadDataset" class="interactive button_secondary"><li><img src="@/assets/images/icon_download_blue.svg" alt="Download dataset"></li></a>
                <a @click="showDatasetShareModal" class="interactive button_secondary"><li><img src="@/assets/images/icon_share_blue.svg" alt="Share dataset"></li></a>
                <a @click="showDatasetRenameModal" class="interactive button_secondary"><li><img src="@/assets/images/icon_rename_blue.svg" alt="Rename dataset"></li></a>
                <a @click="showDatasetDeleteModal" class="interactive button_secondary"><li><img src="@/assets/images/icon_delete_blue.svg" alt="Delete dataset"></li></a>
            </ul>
        </div>

        <ul id="attribute_listing">
            <li @click="selectAttribute(attribute.AID)" v-for="(attribute, index) in currentDataset.attributes" :key="index" class="interactive" :class="{selected_attribute: selectedAttribute === attribute.AID}"><dl>
                <dt>Name</dt><dd>{{ attribute.label }}</dd>
                <dt>Type</dt><dd>
                    <img src="@/assets/images/icon_attribute_nominal_gray.svg" :alt="attribute.type" v-show="attribute.type === 'nominal'">
                    <img src="@/assets/images/icon_attribute_numerical_gray.svg" :alt="attribute.type" v-show="attribute.type === 'numerical'">
                    <img src="@/assets/images/icon_attribute_categorical_gray.svg" :alt="attribute.type" v-show="attribute.type === 'categorical'">
                    <img src="@/assets/images/icon_attribute_vector_gray.svg" :alt="attribute.type" v-show="attribute.type === 'vector'">
                </dd>
                <div id="attribute_listing_item" v-for="(value, index) in attribute.values" :key="index"><dt>Value</dt><dd>{{ value }}</dd></div>
            </dl></li>
        </ul>
    </div>

    <DatasetAttributeDetails />
</section>
</template>

<script>
import { prettifyHumanReadableTime } from '../utils'
import DatasetAttributeDetails from './DatasetAttributeDetails.vue';

export default {
    name: 'DatasetView',
    components: {
        DatasetAttributeDetails
    },
    beforeMount() {
        this.$store.dispatch('getCurrentDataset', { dataset_did: parseInt(this.$route.params.id) })
    },
    methods: {
        showDatasetDeleteModal: function() {
            this.$store.commit('openModal', 'datasetDelete')
        },

        showDatasetRenameModal: function() {
            this.$store.commit('openModal', 'datasetRename')
        },

        showDatasetShareModal: function() {
            this.$store.commit('openModal', 'datasetShare')
        },

        showDatasetUpdateModal: function() {
            this.$store.commit('openModal', 'datasetUpdate')
        },

        showDatasetVersionModal: function() {
            this.$store.commit('openModal', 'datasetVersion')
        },

        selectAttribute: function(attribute) {
            this.$store.commit('selectAttribute', attribute)
        },

        downloadDataset: function() {
            this.$store.dispatch('downloadCurrentDataset')
        }
    },
    computed: {
        lastEdit() {
            let timestamp = this.currentDataset.dataset.lastEdit
            return this.$moment(timestamp * 1000).tz(this.$moment.tz.guess()).calendar()
        },

        currentDataset() {
            return this.$store.state.currentDataset
        },

        selectedAttribute() {
            return this.$store.state.selectedAttribute
        }
    }
}
</script>

<style scoped>
h2 {
    font-family: 'Libre Franklin Bold';
    font-size: 2.5em;
    margin: 0;
    margin-bottom: 0.5em;
}

#dataset_details {
    display: inline;
    list-style: none;
    padding: 0;
    margin: 0;
}

#dataset_details li {
    display: inline-block;
    margin-right: 2em;
    font-family: 'Libre Franklin Bold';
}

#dataset_actions {
    list-style: none;
    padding: 0;
    margin: 0;
    float: right;
}

#dataset_actions li {
    display: inline;
}

#dataset_actions a {
    margin: 0.25em;
}

#dataset_panel {
    padding: 7em;
    padding-top: 3em;
    padding-bottom: 0;
    flex: 2;
    overflow-y: scroll;
    scrollbar-width: none;
}

#attribute_listing {
    list-style: none;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(15em, 1fr));
    grid-gap: 1rem;
}

#attribute_listing dl {
    margin: 0;
}

#attribute_listing li {
    display: inline-block;
    border-radius: 0.3em;
    background-color: #eee;
    padding: 1em;
    border: 1px solid #ccc;
}

#attribute_listing li:hover {
    background: linear-gradient(180deg, #eee 0%, #ddd 40%);
}

#attribute_listing li:active {
    background: linear-gradient(180deg, #bbb 0%, #eee 100%);
}

.selected_attribute {
    background: linear-gradient(180deg, #bbb 0%, #eee 100%) !important;
}

#attribute_listing dt {
    display: none;
}

#attribute_listing dd {
    margin: 0;
    margin-top: 0.5em;
}

#attribute_listing dd:nth-of-type(1) {
    display: inline;
    font-family: 'Libre Franklin Bold';
    font-size: 1.25em;
}

#attribute_listing_item dd:nth-of-type(1) {
    font-family: 'Libre Franklin';
    font-size: 1em;
    display: block;
}

#attribute_listing dd:nth-of-type(2) {
    display: inline;
}

#attribute_listing img {
    float: right;
    width: 3em;
}

#dataset_menu {
    background-color: #ddd;
    padding: 1em;
    border-radius: 0.3em;
}

@media (max-width: 115em) {
    #dataset_actions {
        float: none;
        line-height: 3em;
    }
}
</style>