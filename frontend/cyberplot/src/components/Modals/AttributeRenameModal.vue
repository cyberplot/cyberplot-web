<template>
<form id="form_rename_attribute" v-show="modalOpened" v-if="selectedAttribute" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename attribute</header>
    <p>Please enter a new name for <strong>{{ attributeLabel }}</strong>.</p>

    <input :class="{inputError: inputError}" type="text" ref="labelInput" name="attribute_name" :placeholder="attributeLabel" v-model="inputtedLabel" @keyup.enter="renameAttribute" @keyup="checkIfLabelAvailable">
    <span class="errorText" v-if="labelAlreadyUsed">Label already used.</span>
    <span class="errorText" v-if="labelEmpty">Label cannot be blank.</span>
    <a @click="renameAttribute" id="button_rename" class="button_primary" :class="[!inputError ? 'button_primary' : 'button_secondary_disabled']">Rename attribute</a>
</form>
</template>

<script>
export default {
    name: 'AttributeRenameModal',
    data() {
        return {
            inputtedLabel: '',
            labelAlreadyUsed: false,
            labelEmpty: false
        }
    },
    methods: {
        renameAttribute: function() {
            this.checkIfLabelAvailable()
            if(!this.inputError) {
                this.currentDataset.attributes[this.selectedAttribute - 1].label = this.inputtedLabel
                this.currentDataset.dataset.lastEdit = Math.floor(Date.now() / 1000)
                this.$store.dispatch('changeCurrentDataset')
            }
        },

        checkIfLabelAvailable: function() {
            if(this.inputtedLabel.length == 0) {
                this.labelEmpty = true
                return
            }
            this.labelEmpty = false

            /* check if current dataset does not already contain attribute with same label */
            this.labelAlreadyUsed = false
            this.$store.state.currentDataset.attributes.forEach((attribute) => {
                if(attribute.label == this.inputtedLabel) {
                    this.labelAlreadyUsed = true
                }
            })
        }
    },
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.attributeRename
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
            return this.labelAlreadyUsed || this.labelEmpty
        }
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.inputtedLabel = ''
                this.labelAlreadyUsed = false
                this.labelEmpty = false
            }
            else {
                this.$nextTick(() => {
                    this.$refs.labelInput.focus()
                })
            }
        }
    }
}
</script>

<style scoped>
#button_rename {
    display: block;
    margin-left: auto;

    width: intrinsic;
    width: -moz-max-content;
    width: -webkit-max-content;
}
</style>