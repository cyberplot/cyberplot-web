<template>
<div v-show="modalOpened">
    <Base :updating="updating" v-show="selectedMethod == METHODS.DEFAULT" v-on:formSubmit="selectUpdateMethod" />
    <Python :updating="updating" v-show="selectedMethod == METHODS.PYTHON" v-on:backToInitial="returnToInitial" />
    <R :updating="updating" v-show="selectedMethod == METHODS.R" v-on:backToInitial="returnToInitial" />
</div>
</template>

<script>
import Base from './DatasetUpdateModal/Base.vue'
import Python from './DatasetUpdateModal/Python.vue'
import R from './DatasetUpdateModal/R.vue'

export default {
    name: 'DatasetUpdateModal',
    components: {
        Base,
        Python,
        R
    },
    data() {
        return {
            METHODS: {
                DEFAULT: 'default',
                LOCAL: 'local',
                DATABASE: 'database',
                PYTHON: 'python',
                R: 'r'
            },
            selectedMethod: 'default'
        }
    },
    methods: {
        selectUpdateMethod: function(method) {
            this.selectedMethod = method
        },

        returnToInitial: function() {
            this.selectedMethod = this.METHODS.DEFAULT
        }
    },
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetUpdate
        },

        updating() {
            return this.$store.state.datasetUpdateUpdating
        }
    },
    watch: {
        modalOpened: function(value, oldValue) {
            if(oldValue === false && value === true) {
                this.selectedMethod = this.METHODS.DEFAULT
            }
        }
    }
}
</script>