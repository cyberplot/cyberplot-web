<template>
<div v-show="modalOpened">
    <Base :updating="updating" />
    <!--Python :updating="updating" />
    <R :updating="updating" /-->
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
    computed: {
        modalOpened() {
            return this.$store.state.openedModals.datasetUpdate
        },

        updating() {
            return this.$store.state.datasetUpdateUpdating
        }
    }
}
</script>