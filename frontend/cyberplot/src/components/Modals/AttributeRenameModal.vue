<template>
<form id="form_rename_attribute" v-show="modalOpened" v-if="selectedAttribute" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename attribute</header>
    <p>Please enter a new name for <strong>{{ attributeLabel }}</strong>.</p>

    <input :class="{inputError: labelAlreadyUsed}" type="text" ref="labelInput" name="attribute_name" :placeholder="attributeLabel" v-model="inputtedLabel" @keyup.enter="renameAttribute" @keyup="checkIfLabelAvailable">
    <span class="errorText" v-if="labelAlreadyUsed">Label already used.</span>
    <a @click="renameAttribute" id="button_rename" class="button_primary">Rename attribute</a>
</form>
</template>

<script>
export default {
    name: 'AttributeRenameModal',
    data() {
        return {
            inputtedLabel: '',
            labelAlreadyUsed: false
        }
    },
    methods: {
        renameAttribute: function() {
            if(!this.labelAlreadyUsed) {
                this.currentDataset.attributes[this.selectedAttribute - 1].label = this.inputtedLabel
                this.currentDataset.dataset.lastEdit = Math.floor(Date.now() / 1000)
                this.$store.dispatch('changeCurrentDataset')
            }
        },

        checkIfLabelAvailable: function() {
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
            var attributeAID = this.selectedAttribute

            for(let [index, attribute] of this.currentDataset.attributes.entries()) {
                if(attribute.AID == attributeAID) {
                    return attribute.label
                }
            }
        }
    },
    watch: {
        modalOpened: function(val) {
            if(val == false) {
                this.inputtedLabel = ''
                this.labelAlreadyUsed = false
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