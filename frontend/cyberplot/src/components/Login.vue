<template>
<content>
    <main>
        <form id="login_form">
            <img src="@/assets/images/logo_blue.svg" alt="Cyberplot logo">
            <input type="text" name="user_name" placeholder="User name" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_user_gray.svg')})`}">
            <input type="password" name="password" placeholder="Password" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_password_gray.svg')})`}">
            <a href="#" id="button_login" class="button_primary">Log in</a>
            <a href="#" id="button_forgot" class="button_secondary">Forgot password?</a>
        </form>

        <p>
            New to cyberplot?
            <a href="#" id="button_signup" class="button_secondary">Sign up</a>
        </p>
    </main>
</content>
</template>

<script>
export default {
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

#login_form {
    background-color: #f9f9f9;
    padding: 1.5em;
    border-radius: 0.3em;
}

#login_form input {
    width: -webkit-fill-available;
    width: -moz-available;
}

main {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: block;
    margin: 0;
    position: relative;
    width: 22em;
    height: 24em;
}

#login_form img {
    width: 12em;
    display: block;
    margin: auto;
    margin-bottom: 2em;
    margin-top: 1em;
}

#login_form .button_primary {
    display: block;
    text-align: center;
}

#login_form .button_secondary {
    margin-top: 1em;
    display: block;
    text-align: center;
}

#button_signup {
    margin-left: 0.5em;
}

p {
    text-align: center;
    color: white;
}
</style>
