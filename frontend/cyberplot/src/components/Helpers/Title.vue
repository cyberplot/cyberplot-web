<script>
export default {
    name: 'vue-title',
    props: ['title'],
    mounted() {
        document.title = this.title;
    },
    watch: {
        title() {
            document.title = this.title;
        }
    },
    render() {
    }
}
</script>