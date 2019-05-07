<template>
<div id="attribute_statistics">
    <dl>
        <dt><img src="@/assets/images/icon_statistics_gray.svg"> Statistics</dt>
        <dd>
            <table>
                <tr><td>{{ currentDataset.statistics[selectedAttribute].minimum }}</td><td>{{ currentDataset.statistics[selectedAttribute].Q1 }}</td><td>{{ currentDataset.statistics[selectedAttribute].median }}</td><td>{{ currentDataset.statistics[selectedAttribute].Q3 }}</td><td>{{ currentDataset.statistics[selectedAttribute].maximum }}</td></tr>
                <tr><td>min</td><td>1Q</td><td>med</td><td>3Q</td><td>max</td></tr>
            </table>

            <ul>
                <li><img src="@/assets/images/icon_mean_gray.svg" alt="Arithmetic mean"> {{ currentDataset.statistics[selectedAttribute].mean }}</li>
                <li><img src="@/assets/images/icon_standard_deviation_gray.svg" alt="Standard deviation"> {{ currentDataset.statistics[selectedAttribute].sdev }}</li>
            </ul>
        </dd>
    </dl>
</div>
</template>

<script>
export default {
    name: 'DatasetAttributeStatistics',
    computed: {
        currentDataset() {
            return this.$store.state.currentDataset
        },

        selectedAttribute() {
            return this.$store.state.selectedAttribute
        }
    }
}
</script>