<template>
<div id="attribute_panel" v-if="selectedAttribute != -1">
    <div id="attribute_settings">
        <h2>{{ currentDataset.attributes[selectedAttribute].label }}</h2>
        <a @click="showAttributeRenameModal" id="attribute_rename_button" class="button_secondary"><img src="@/assets/images/icon_rename_blue.svg" alt="Rename attribute"></a>
        <dl>
            <dt><img src="@/assets/images/icon_data_type_gray.svg"> Data type</dt>
            <dd id="data_type_selector" class="selector">
                <a @click="changeAttributeType('nominal')" id="data_type_nominal_button" :class="nominalSelectorStyle"><img :src="[possibleTypes.nominal && this.type != 'nominal' ? require('@/assets/images/label_attribute_nominal_blue.svg') : require('@/assets/images/label_attribute_nominal_white.svg')]" alt="Nominal"></a>
                <a @click="changeAttributeType('numerical')" id="data_type_numerical_button" :class="numericalSelectorStyle"><img :src="[possibleTypes.numerical && this.type != 'numerical' ? require('@/assets/images/label_attribute_numerical_blue.svg') : require('@/assets/images/label_attribute_numerical_white.svg')]" alt="Numerical"></a>
                <a @click="changeAttributeType('categorical')" id="data_type_categorical_button" :class="categoricalSelectorStyle"><img :src="[possibleTypes.categorical && this.type != 'categorical' ? require('@/assets/images/label_attribute_categorical_blue.svg') : require('@/assets/images/label_attribute_categorical_white.svg')]" alt="Categorical"></a>
                <a @click="changeAttributeType('vector')" id="data_type_vector_button" :class="vectorSelectorStyle"><img :src="[possibleTypes.vector && this.type != 'vector' ? require('@/assets/images/label_attribute_vector_blue.svg') : require('@/assets/images/label_attribute_vector_white.svg')]" alt="Vector"></a>
            </dd>
            <dt><img src="@/assets/images/icon_data_missing_gray.svg"> Missing values</dt>
            <dd id="data_missing_selector" class="selector">
                <a @click="changeMissingValueSetting('ignore')" id="data_missing_ignore_button" :class="ignoreSelectorStyle">Ignore</a>
                <a @click="changeMissingValueSetting('mean')" id="data_missing_mean_button" :class="meanSelectorStyle">Use mean</a>
                <a @click="changeMissingValueSetting('median')" id="data_missing_median_button" :class="medianSelectorStyle">Use median</a>
                <a @click="changeMissingValueSetting('custom')" id="data_missing_custom_button" :class="customSelectorStyle">Custom<span v-if="missingValueCustom != null">: {{ missingValueCustom }}</span></a>
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
        },

        changeAttributeType: function(type) {
            if(this.possibleTypes[type]) {
                this.currentDataset.attributes[this.selectedAttribute].type = type
                this.$store.dispatch('changeCurrentDataset')
            }
        },

        changeMissingValueSetting: function(setting, customValue) {
            this.currentDataset.attributes[this.selectedAttribute].missingValueSetting = setting
            if(customValue) {
                this.currentDataset.attributes[this.selectedAttribute].missingValueCustom = customValue
            }
            this.$store.dispatch('changeCurrentDataset')
        }
    },
    computed: {
        currentDataset() {
            return this.$store.state.currentDataset
        },

        possibleTypes() {
            return this.currentDataset.attributes[this.selectedAttribute].possibleTypes
        },

        type() {
            return this.currentDataset.attributes[this.selectedAttribute].type
        },

        missingValueSetting() {
            return this.currentDataset.attributes[this.selectedAttribute].missingValueSetting
        },

        missingValueCustom() {
            return this.currentDataset.attributes[this.selectedAttribute].missingValueCustom
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
        },

        nominalSelectorStyle: function() {
            return {
                'button_primary': this.type === 'nominal',
                'button_secondary': this.possibleTypes.nominal && this.type != 'nominal',
                'button_secondary_disabled': !this.possibleTypes.nominal
            }
        },

        numericalSelectorStyle: function() {
            return {
                'button_primary': this.type === 'numerical',
                'button_secondary': this.possibleTypes.numerical && this.type != 'numerical',
                'button_secondary_disabled': !this.possibleTypes.numerical
            }
        },

        categoricalSelectorStyle: function() {
            return {
                'button_primary': this.type === 'categorical',
                'button_secondary': this.possibleTypes.categorical && this.type != 'categorical',
                'button_secondary_disabled': !this.possibleTypes.categorical
            }
        },

        vectorSelectorStyle: function() {
            return {
                'button_primary': this.type === 'vector',
                'button_secondary': this.possibleTypes.vector && this.type != 'vector',
                'button_secondary_disabled': !this.possibleTypes.vector
            }
        },

        ignoreSelectorStyle: function() {
            return {
                'button_primary': this.missingValueSetting === 'ignore',
                'button_secondary': this.missingValueSetting != 'ignore'
            }
        },

        meanSelectorStyle: function() {
            return {
                'button_primary': this.missingValueSetting === 'mean',
                'button_secondary': this.missingValueSetting != 'mean'
            }
        },

        medianSelectorStyle: function() {
            return {
                'button_primary': this.missingValueSetting === 'median',
                'button_secondary': this.missingValueSetting != 'median'
            }
        },

        customSelectorStyle: function() {
            return {
                'button_primary': this.missingValueSetting === 'custom',
                'button_secondary': this.missingValueSetting != 'custom'
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