<template>
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
</template>

<script>
export default {
    name: 'UserSettingsModal'
}
</script>