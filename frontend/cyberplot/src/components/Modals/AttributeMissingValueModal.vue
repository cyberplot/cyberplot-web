<template>
<form id="form_attribute_missing_value" v-show="modalOpened" v-if="selectedAttribute" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_rename_blue.svg"> Custom missing value</header>
    <p>Please specify a custom value setting for <strong>{{ attributeLabel }}</strong>.</p>

    <input :class="{inputError: inputError}" type="text" ref="valueInput" name="attribute_name" v-model="inputtedValue" @keyup.enter="setMissingValue" @keyup="checkIfValueValid">
    <span class="errorText" v-if="valueNotValid">Value not valid for set attribute type.</span>
    <span class="errorText" v-if="valueEmpty">Please specify a value.</span>
    <a @click="setMissingValue" id="button_set" class="button_primary" :class="[!inputError ? 'button_primary' : 'button_secondary_disabled']">Set custom value</a>
</form>
</template>

<script>
export default {
    name: 'AttributeMissingValueModal',
    data() {
        return {
            inputtedValue: '',
            valueNotValid: false,
            valueEmpty: false
        }
    },
    methods: {
        setMissingValue: function() {
            this.checkIfValueValid()
            if(!this.inputError) {
                this.currentDataset.attributes[this.selectedAttribute - 1].missingValueSetting = 'custom'
                this.currentDataset.attributes[this.selectedAttribute - 1].missingValueCustom = this.inputtedValue
                this.currentDataset.dataset.lastEdit = Math.floor(Date.now() / 1000)
                this.$store.dispatch('changeCurrentDataset')
            }
        },

        checkIfValueValid: function() {
            this.valueNotValid = false
            if(this.$store.getters.selectedAttributeData.type === 'numerical' && isNaN(this.inputtedValue)) {
                this.valueNotValid = true
            }

            this.valueEmpty = false
            if(this.inputtedValue.length == 0) {
                this.valueEmpty = true
            }
        }
    },
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.attributeMissingValue
        },

        selectedAttribute() {
            return this.$store.state.selectedAttribute
        },

        currentDataset() {
            return this.$store.state.currentDataset
        },

        attributeLabel() {
            return this.$store.getters.selectedAttributeData.label
        },

        inputError() {
            return this.valueNotValid || this.valueEmpty
        }
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.inputtedValue = ''
                this.valueNotValid = false
                this.valueEmpty = false
            }
            else {
                this.$nextTick(() => {
                    this.$refs.valueInput.focus()
                })
            }
        }
    }
}
</script>

<style scoped>
#button_set {
    display: block;
    margin-left: auto;

    width: intrinsic;
    width: -moz-max-content;
    width: -webkit-max-content;
}
</style>