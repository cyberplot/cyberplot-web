<template>
<form id="form_rename_attribute" v-show="modalOpened" v-if="selectedAttribute" autocomplete="off" @submit.prevent>
    <header><img src="@/assets/images/icon_rename_blue.svg"> Rename attribute</header>
    <p>Please enter a new name for <strong>{{ attributeLabel }}</strong>.</p>

    <input type="text" ref="labelInput" name="attribute_name" :placeholder="attributeLabel" v-model="inputtedLabel" @keyup.enter="renameAttribute">
    <a href="#" id="button_rename" class="button_primary">Rename attribute</a>
</form>
</template>

<script>
export default {
    name: 'AttributeRenameModal',
    data() {
        return {
            inputtedLabel: ''
        }
    },
    methods: {
        renameAttribute: function() {
            /* #TODO */
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