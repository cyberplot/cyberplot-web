<template>
<section id="content" v-if="currentDataset">
    <div id="dataset_panel">
        <h2>{{ currentDataset.dataset.name }}</h2>
        <ul id="dataset_details">
            <li><img src="@/assets/images/icon_rows_gray.svg"> {{ currentDataset.dataset.item_count }} items</li>
            <li><img src="@/assets/images/icon_attribute_gray.svg"> {{ currentDataset.attributes.length }} attributes</li>
            <li><img src="@/assets/images/icon_time_gray.svg"> Edited on {{ lastEdit }}</li>
        </ul>

        <ul id="dataset_actions">
            <a @click="showDatasetUpdateModal" class="interactive"><li><img src="@/assets/images/icon_update_blue.svg" alt="Update dataset"></li></a>
            <a href="#" class="interactive"><li><img src="@/assets/images/icon_download_blue.svg" alt="Download dataset"></li></a>
            <a @click="showDatasetShareModal" class="interactive"><li><img src="@/assets/images/icon_share_blue.svg" alt="Share dataset"></li></a>
            <a @click="showDatasetRenameModal" class="interactive"><li><img src="@/assets/images/icon_rename_blue.svg" alt="Rename dataset"></li></a>
            <a @click="showDatasetDeleteModal" class="interactive"><li><img src="@/assets/images/icon_delete_blue.svg" alt="Delete dataset"></li></a>
        </ul>

        <ul id="attribute_listing">
            <li @click="selectedAttribute = index" v-for="(attribute, index) in currentDataset.attributes" :key="index" class="interactive"><dl>
                <dt>Name</dt><dd>{{ attribute.label }}</dd>
                <dt>Type</dt><dd>
                    <img src="@/assets/images/icon_attribute_nominal_white.svg" :alt="attribute.type" v-show="attribute.type === 'nominal'">
                    <img src="@/assets/images/icon_attribute_numerical_white.svg" :alt="attribute.type" v-show="attribute.type === 'numerical'">
                    <img src="@/assets/images/icon_attribute_categorical_white.svg" :alt="attribute.type" v-show="attribute.type === 'categorical'">
                    <img src="@/assets/images/icon_attribute_vector_white.svg" :alt="attribute.type" v-show="attribute.type === 'vector'">
                </dd>
                <div id="attribute_listing_item" v-for="(value, index) in attribute.values" :key="index"><dt>Value</dt><dd>{{ value }}</dd></div>
            </dl></li>
        </ul>
    </div>

    <DatasetAttributeDetails :attribute="currentDataset.attributes[selectedAttribute]" :statistics="currentDataset.statistics[selectedAttribute]" />
</section>
</template>

<script>
import DatasetAttributeDetails from './DatasetAttributeDetails.vue';

export default {
    name: 'DatasetView',
    components: {
        DatasetAttributeDetails
    },
    beforeMount() {
        this.$store.dispatch('getCurrentDataset', { dataset_did: parseInt(this.$route.params.id) })
    },
    data() {
        return {
            selectedAttribute: 0
        }
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
    },
    computed: {
        lastEdit() {
            var date = Date(this.currentDataset.dataset.lastEdit);
            return date.toLocaleString();
        },

        currentDataset() {
            return this.$store.state.currentDataset
        }
    }
}
</script>