<template>
<div id="attribute_panel" v-if="selectedAttribute != -1">
    <div id="attribute_settings">
        <h2>{{ currentDataset.attributes[selectedAttribute].label }}</h2>
        <a @click="showAttributeRenameModal" id="attribute_rename_button" class="button_secondary"><img src="@/assets/images/icon_rename_blue.svg" alt="Rename attribute"></a>
        <dl>
            <dt><img src="@/assets/images/icon_data_type_gray.svg"> Data type</dt>
            <dd id="data_type_selector" class="selector">
                <a href="#" id="data_type_nominal_button" :class="[currentDataset.attributes[selectedAttribute].possibleTypes.nominal ? 'button_secondary' : 'button_secondary_disabled']"><img :src="[currentDataset.attributes[selectedAttribute].possibleTypes.nominal ? require('@/assets/images/label_attribute_nominal_blue.svg') : require('@/assets/images/label_attribute_nominal_white.svg')]" alt="Nominal"></a>
                <a href="#" id="data_type_numerical_button" :class="[currentDataset.attributes[selectedAttribute].possibleTypes.numerical ? 'button_secondary' : 'button_secondary_disabled']"><img :src="[currentDataset.attributes[selectedAttribute].possibleTypes.numerical ? require('@/assets/images/label_attribute_numerical_blue.svg') : require('@/assets/images/label_attribute_numerical_white.svg')]" alt="Numerical"></a>
                <a href="#" id="data_type_categorical_button" :class="[currentDataset.attributes[selectedAttribute].possibleTypes.categorical ? 'button_secondary' : 'button_secondary_disabled']"><img :src="[currentDataset.attributes[selectedAttribute].possibleTypes.categorical ? require('@/assets/images/label_attribute_categorical_blue.svg') : require('@/assets/images/label_attribute_categorical_white.svg')]" alt="Categorical"></a>
                <a href="#" id="data_type_vector_button" :class="[currentDataset.attributes[selectedAttribute].possibleTypes.vector ? 'button_secondary' : 'button_secondary_disabled']"><img :src="[currentDataset.attributes[selectedAttribute].possibleTypes.vector ? require('@/assets/images/label_attribute_vector_blue.svg') : require('@/assets/images/label_attribute_vector_white.svg')]" alt="Vector"></a>
            </dd>
            <dt><img src="@/assets/images/icon_data_missing_gray.svg"> Missing values</dt>
            <dd id="data_missing_selector" class="selector">
                <a href="#" id="data_missing_ignore_button" class="button_secondary">Ignore</a>
                <a href="#" id="data_missing_mean_button" class="button_secondary">Use mean</a>
                <a href="#" id="data_missing_median_button" class="button_secondary">Use median</a>
                <a href="#" id="data_missing_custom_button" class="button_secondary">Custom</a>
            </dd>
        </dl>
    </div>

    <DatasetAttributeStatistics />
</div>
</template>

<script>
import DatasetAttributeStatistics from './DatasetAttributeStatistics.vue';
import AttributeRenameModal from './Modals/AttributeRenameModal.vue'

export default {
    name: 'DatasetAttributeDetails',
    components: {
        DatasetAttributeStatistics,
        AttributeRenameModal
    },
    methods: {
        showAttributeRenameModal: function() {
            this.$store.commit('openModal', 'attributeRename')
        }
    },
    computed: {
        currentDataset() {
            return this.$store.state.currentDataset
        },

        selectedAttribute() {
            var attributeAID = this.$store.state.selectedAttribute

            if(!attributeAID) {
                return -1
            }

            for(let [index, attribute] of this.currentDataset.attributes.entries()) {
                if(attribute.AID == attributeAID) {
                    return index
                }
            }
        }
    }
}
</script>

<style scoped>
h2 {
    font-family: 'Libre Franklin Bold';
    font-size: 2em;
    margin: 0;
    margin-bottom: 0.5em;
}

#attribute_panel {
    flex: 1;
    background-color: #ddd;
    padding-top: 2em;
    padding-left: 7em;
    padding-right: 7em;
    display: flex;
}

#attribute_panel h2 {
    font-size: 1.75em;
    margin-right: 0.5em;
    display: inline;
}

#attribute_settings {
    flex: auto;
}

#attribute_rename_button {
    display: inline;
}

#attribute_settings dd {
    margin-bottom: 1em;
    margin-top: 0.3em;
    line-height: 3em;
}
</style>