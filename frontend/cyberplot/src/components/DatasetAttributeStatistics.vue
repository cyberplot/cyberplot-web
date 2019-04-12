<template>
<div id="attribute_statistics">
    <dl>
        <dt><img src="@/assets/images/icon_statistics_gray.svg"> Statistics</dt>
        <dd>
            <table>
                <tr><td>{{ stats.min }}</td><td>{{ stats.q1 }}</td><td>{{ stats.med }}</td><td>{{ stats.q3 }}</td><td>{{ stats.max }}</td></tr>
                <tr><td>min</td><td>1Q</td><td>med</td><td>3Q</td><td>max</td></tr>
            </table>

            <ul>
                <li><img src="@/assets/images/icon_mean_gray.svg" alt="Arithmetic mean"> {{ stats.mean }}</li>
                <li><img src="@/assets/images/icon_standard_deviation_gray.svg" alt="Standard deviation"> {{ stats.sdev }}</li>
            </ul>
        </dd>
    </dl>
</div>
</template>

<script>
export default {
    name: 'DatasetAttributeStatistics',
    props: {
        stats: {
            type: Array,
            required: false,
            default: "none"
        }
    }
}
</script>