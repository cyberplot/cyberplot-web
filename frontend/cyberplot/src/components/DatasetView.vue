<template>
<section id="content">
    <div id="dataset_panel">
        <h2>{{ dataset.name }}</h2>
        <ul id="dataset_details">
            <li><img src="@/assets/images/icon_rows_gray.svg"> {{ dataset.item_count }} items</li>
            <li><img src="@/assets/images/icon_attribute_gray.svg"> {{ dataset.attributes.length }} attributes</li>
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
            <li @click="selectedAttribute = index" v-for="(attribute, index) in dataset.attributes" :key="index" class="interactive"><dl>
                <dt>Name</dt><dd>{{ attribute.label }}</dd>
                <dt>Type</dt><dd>
                    <img src="@/assets/images/icon_attribute_nominal_white.svg" :alt="attribute.selected_type" v-show="attribute.selected_type === 'nominal'">
                    <img src="@/assets/images/icon_attribute_numerical_white.svg" :alt="attribute.selected_type" v-show="attribute.selected_type === 'numerical'">
                    <img src="@/assets/images/icon_attribute_categorical_white.svg" :alt="attribute.selected_type" v-show="attribute.selected_type === 'categorical'">
                    <img src="@/assets/images/icon_attribute_vector_white.svg" :alt="attribute.selected_type" v-show="attribute.selected_type === 'vector'">
                </dd>
                <div id="attribute_listing_item" v-for="(value, index) in attribute.values" :key="index"><dt>Value</dt><dd>{{ value }}</dd></div>
            </dl></li>
        </ul>
    </div>

    <DatasetAttributeDetails :attribute="dataset.attributes[selectedAttribute]" />
</section>
</template>

<script>
import DatasetAttributeDetails from './DatasetAttributeDetails.vue';

export default {
    name: 'DatasetView',
    components: {
        DatasetAttributeDetails
    },
    data() {
        return {
            selectedAttribute: 0,
            dataset: {
                id: 3,
                name: "Iris Dataset",
                item_count: 150,
                last_edit: 1555044143000,
                attributes: [
                    {
                        label: "Sepal Length",
                        selected_type: "numerical",
                        possible_types: {
                            nominal: true,
                            numerical: true,
                            categorical: false,
                            vector: false
                        },
                        values: [
                            "5.1",
                            "4.9",
                            "4.7"
                        ],
                        stats: {
                            min: 4.5,
                            q1: 4.8,
                            med: 5.1,
                            q3: 5.3,
                            max: 6.0,
                            mean: 5.3,
                            sdev: 0.4
                        },
                        missing_setting: null
                    },
                    {
                        label: "Sepal Width",
                        selected_type: "numerical",
                        possible_types: {
                            nominal: true,
                            numerical: true,
                            categorical: false,
                            vector: false
                        },
                        values: [
                            "3.5",
                            "3.0",
                            "3.2"
                        ],
                        stats: {
                            min: 2.5,
                            q1: 3.1,
                            med: 3.5,
                            q3: 3.7,
                            max: 4.5,
                            mean: 3.3,
                            sdev: 0.6
                        },
                        missing_setting: null
                    },
                    {
                        label: "Petal Length",
                        selected_type: "numerical",
                        possible_types: {
                            nominal: true,
                            numerical: true,
                            categorical: false,
                            vector: false
                        },
                        values: [
                            "1.4",
                            "1.4",
                            "1.3"
                        ],
                        stats: {
                            min: 1.0,
                            q1: 1.2,
                            med: 1.4,
                            q3: 1.5,
                            max: 1.8,
                            mean: 1.4,
                            sdev: 0.2
                        },
                        missing_setting: null
                    },
                    {
                        label: "Petal Width",
                        selected_type: "numerical",
                        possible_types: {
                            nominal: true,
                            numerical: true,
                            categorical: false,
                            vector: false
                        },
                        values: [
                            "0.2",
                            "0.2",
                            "0.2"
                        ],
                        stats: {
                            min: 0.1,
                            q1: 0.1,
                            med: 0.2,
                            q3: 0.3,
                            max: 0.5,
                            mean: 0.2,
                            sdev: 0.1
                        },
                        missing_setting: null
                    },
                    {
                        label: "Class",
                        selected_type: "categorical",
                        possible_types: {
                            nominal: true,
                            numerical: false,
                            categorical: true,
                            vector: false
                        },
                        values: [
                            "setosa",
                            "setosa",
                            "setosa"
                        ],
                        stats: {
                        },
                        missing_setting: null
                    },
                ]
            }
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
            var date = new Date(this.dataset.last_edit);
            return date.toLocaleString();
        }
    }
}
</script>