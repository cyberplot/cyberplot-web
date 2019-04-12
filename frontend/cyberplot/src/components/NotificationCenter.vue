<template>
<div id="notifications">
    <img id="arrow" src="@/assets/images/popup_arrow.svg">

    <form>
        <header><img src="@/assets/images/icon_share_incoming_blue.svg"> Shared dataset</header>
        <p>
            georgecost shared <strong>Revenue Q3</strong> with you.
        </p>
    
        <a href="#" id="button_accept" class="button_primary">Accept</a>
        <a href="#" id="button_ignore" class="button_secondary">Ignore</a>
    </form>
</div>
</template>

<script>
export default {
    name: 'NotificationCenter'
}
</script>