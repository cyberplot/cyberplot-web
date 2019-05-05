<template>
<div id="attribute_panel">
    <div id="attribute_settings">
        <h2>{{ attribute.label }}</h2>
        <a @click="showAttributeRenameModal" id="attribute_rename_button" class="button_secondary"><img src="@/assets/images/icon_rename_blue.svg" alt="Rename attribute"></a>
        <dl>
            <dt><img src="@/assets/images/icon_data_type_gray.svg"> Data type</dt>
            <dd id="data_type_selector" class="selector">
                <a href="#" id="data_type_nominal_button" :class="[attribute.possibleTypes.nominal ? 'button_secondary' : 'button_secondary_disabled']"><img :src="[attribute.possibleTypes.nominal ? require('@/assets/images/label_attribute_nominal_blue.svg') : require('@/assets/images/label_attribute_nominal_white.svg')]" alt="Nominal"></a>
                <a href="#" id="data_type_numerical_button" :class="[attribute.possibleTypes.numerical ? 'button_secondary' : 'button_secondary_disabled']"><img :src="[attribute.possibleTypes.numerical ? require('@/assets/images/label_attribute_numerical_blue.svg') : require('@/assets/images/label_attribute_numerical_white.svg')]" alt="Numerical"></a>
                <a href="#" id="data_type_categorical_button" :class="[attribute.possibleTypes.categorical ? 'button_secondary' : 'button_secondary_disabled']"><img :src="[attribute.possibleTypes.categorical ? require('@/assets/images/label_attribute_categorical_blue.svg') : require('@/assets/images/label_attribute_categorical_white.svg')]" alt="Categorical"></a>
                <a href="#" id="data_type_vector_button" :class="[attribute.possibleTypes.vector ? 'button_secondary' : 'button_secondary_disabled']"><img :src="[attribute.possibleTypes.vector ? require('@/assets/images/label_attribute_vector_blue.svg') : require('@/assets/images/label_attribute_vector_white.svg')]" alt="Vector"></a>
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

    <DatasetAttributeStatistics :stats="statistics" />
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
    props: {
        attribute: Object,
        statistics: Object
    }
}
</script>