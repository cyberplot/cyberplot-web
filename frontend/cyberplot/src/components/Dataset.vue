<template>
<content>
    <nav id="navigation_main">
        <h1>Cyberplot</h1>
        <img src="@/assets/images/logo_white.svg" alt="Cyberplot logo" id="cyberplot_logo">
        <a href="#" id="logout_button" class="button_secondary">Log out</a>
        <a href="#" id="user_label">
            <img src="@/assets/images/icon_user_white.svg" alt="User profile" id="icon_user">
            username
        </a>
    </nav>

    <main>
        <section id="sidebar">
            <ul id="dataset_listing">
                <a href="#"><li>dataset1</li></a>
                <a href="#"><li id="active_dataset_button">dataset2</li></a>
                <a href="#"><li>dataset3</li></a>
                <a href="#"><li>dataset4</li></a>
                <a href="#"><li>dataset5</li></a>
            </ul>

            <a href="#" id="dataset_add_button" class="button_primary">Add new dataset</a>
        </section>

        <section id="content">
            <!-- CONTENT -->
        </section>
    </main>

    <div id="overlay">
        <dialog>
            <a href="#" id="button_close" class="button_secondary"><img src="@/assets/images/icon_close_blue.svg" alt="Close dialog"></a>
            <!-- OVERLAY -->

            <form id="form_user_settings">
                <header><img src="@/assets/images/icon_user_blue.svg"> User settings</header>
                <p>If you would like to change your password, you can do so here.</p>
        
                <input type="password" name="password" placeholder="Enter new password">
                <input type="password" name="password_confirm" placeholder="Confirm password">
                <a href="#" id="button_password_change" class="button_primary">Change password</a>

                <p>Here you can delete your cyberplot account. This will remove all your datasets and spaces. Be aware that the operation cannot be reversed. If your are certain, please enter <strong>I want to delete my cyberplot account</strong> into the following textbox.</p>

                <input type="text" name="deleted_account_name" placeholder="I want to delete my cyberplot account">
                <a href="#" id="button_account_delete" class="button_primary">Delete account</a>
            </form>
        </dialog>
    </div>

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
</content>
</template>

<script>
export default {
    name: 'Dataset',
    data() {
        return {
        }
    }
}
</script>

<style scoped>
content {
    display: contents;
}

h2 {
    font-family: 'Libre Franklin Bold';
    font-size: 2.5em;
    margin: 0;
    margin-bottom: 0.5em;
}

li img {
    vertical-align: middle;
    width: 2em;
}

dt img {
    vertical-align: middle;
    width: 2em;
}

#dataset_details {
    display: inline;
    list-style: none;
    padding: 0;
    margin: 0;
}

#dataset_details li {
    display: inline;
    margin-right: 2em;
    font-family: 'Libre Franklin Bold';
}

#dataset_actions {
    display: inline;
    list-style: none;
    padding: 0;
    margin: 0;
    float: right;
}

#dataset_actions li {
    display: inline;
    margin-left: 1em;
}

#dataset_panel {
    padding: 7em;
    padding-top: 3em;
    padding-bottom: 0;
    flex: 2;
    overflow-y: scroll;
}

#attribute_listing {
    list-style: none;
    padding: 0;
}

#attribute_listing li {
    display: inline-block;
    border-radius: 0.3em;
    background-color: #333;
    background: linear-gradient(180deg, #4b4b4b 00%, #333 100%);
    width: 15em;
    padding: 1em;
    color: white;
    margin-right: 1em;
    margin-bottom: 1em;
}

#attribute_listing li:hover {
    background: linear-gradient(180deg, #5c5c5c 0%, #474747 100%);
}

#attribute_listing dt {
    display: none;
}

#attribute_listing dd {
    margin: 0;
    margin-top: 0.5em;
}

#attribute_listing dd:nth-of-type(1) {
    display: inline;
    font-family: 'Libre Franklin Bold';
    font-size: 1.25em;
}

#attribute_listing dd:nth-of-type(2) {
    display: inline;
}

#attribute_listing img {
    float: right;
    width: 3em;
}

#attribute_panel {
    flex: 1;
    background-color: #ccc;
    padding-top: 2em;
    padding-left: 7em;
    padding-right: 7em;
    display: flex;
}

dt {
    font-family: 'Libre Franklin Bold';
}

#attribute_panel h2 {
    font-size: 1.75em;
    margin-right: 0.5em;
    display: inline;
}

#attribute_settings {
    flex: 2;
}

#attribute_statistics {
    flex: 1;
}

a img {
    vertical-align: middle;
}

.selector a {
    margin-right: 0.5em;
}

#attribute_rename_button {
    display: inline;
}

#attribute_settings dd {
    margin-bottom: 1em;
    margin-top: 0.3em;
}

#attribute_statistics table {
    background-color: #eee;
    border-radius: 0.3em;
    padding: 0.5em;
    border-spacing: 0;
}

#attribute_statistics td {
    padding: 0.2em;
    width: 3em;
    text-align: center;
}

#attribute_statistics tr:nth-of-type(1) {
    font-family: 'Libre Franklin Bold';
}

#attribute_statistics tr:nth-of-type(2) {
    font-size: 0.8em;
}

#attribute_statistics tr:nth-of-type(1) td:nth-of-type(2) {
    border: 1px solid #4b4b4b;
    border-right: none;
}

#attribute_statistics tr:nth-of-type(1) td:nth-of-type(3) {
    border-top: 1px solid #4b4b4b;
    border-bottom: 1px solid #4b4b4b;
}

#attribute_statistics tr:nth-of-type(1) td:nth-of-type(4) {
    border: 1px solid #4b4b4b;
    border-left: none;
}

#attribute_statistics ul {
    list-style: none;
    padding: 0;
}

#attribute_statistics li {
    display: inline-block;
    width: 8.6em;
    border-radius: 0.3em;
    border: 1px solid #4b4b4b;
    padding: 0.1em;
    margin-top: 0.5em;
    font-family: 'Libre Franklin Bold';
}

#attribute_statistics li:nth-of-type(1) {
    margin-right: 0.1em;
}

#attribute_statistics li:nth-of-type(2) {
    margin-left: 0.1em;
}

#overlay #form_update div {
    width: 9em;
    height: 8em;
    margin: 0.75em;
    text-align: center;
    padding-top: 1.5em;
    display: inline-block;
    padding-left: 0.5em;
    padding-right: 0.5em;
}

#overlay #form_update_r .button_secondary {
    margin-left: 4.1em;
}

#overlay #form_update_python .button_secondary {
    margin-left: 4.1em;
}
</style>