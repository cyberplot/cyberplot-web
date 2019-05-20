<template>
<content>
    <main :class="{signup_main: signingUp}">
        <form id="login_form">
            <img src="@/assets/images/logo_blue.svg" alt="Cyberplot logo">
            <input :class="{inputError: loginFailed}" type="text" ref="username" name="username" placeholder="Username" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_user_gray.svg')})`}" v-model="username" @keyup.enter="authenticate">
            <input :class="{inputError: loginFailed || passwordsDoNotMatch}" type="password" name="password" placeholder="Password" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_password_gray.svg')})`}" v-model="password" @keyup.enter="authenticate">
            <input v-if="signingUp" :class="{inputError: passwordsDoNotMatch}" type="password" name="password_confirm" placeholder="Confirm password" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_password_gray.svg')})`}" v-model="passwordConfirmation" @keyup.enter="authenticate">
            <input v-if="signingUp" type="email" name="email" placeholder="E-mail" class="textbox_with_icon" v-model="email" @keyup.enter="authenticate">
            <span class="errorText" v-if="loginFailed">Incorrect username and/or password.</span>
            <span class="errorText" v-if="usernameTaken">Username is already taken.</span>
            <span class="errorText" v-if="passwordsDoNotMatch">Passwords do not match.</span>
            <a @click="authenticate" id="button_login" class="button_primary">{{ signingUp ? "Sign up" : "Log in" }}</a>
            <a v-if="!signingUp" href="#" id="button_forgot" class="button_secondary">Forgot password?</a>
        </form>

        <p>
            {{ signingUp ? "Already have an account?" : "New to cyberplot?" }}
            <a @click="changeContext" id="button_signup" class="button_secondary">{{ signingUp ? "Log in" : "Sign up" }}</a>
        </p>
    </main>
</content>
</template>

<script>
import {EventBus} from '../utils';

export default {
    data() {
        return {
            username: '',
            password: '',
            passwordConfirmation: '',
            email: '',
            loginFailed: false,
            passwordsDoNotMatch: false,
            usernameTaken: false,
            signingUp: false
        }
    },
    methods: {
        authenticate: function() {
            if(!this.signingUp) {
                this.$store.dispatch('login', { username: this.username,
                                                password: this.password })
                    .then(() => this.$router.push('/'))
            }
            else {
                if(this.password != this.passwordConfirmation) {
                    this.passwordsDoNotMatch = true
                    return
                }

                this.$store.dispatch('signup', { username: this.username,
                                                 password: this.password,
                                                 email: this.email })
                    .then(() => this.$router.push('/'))
            }
        },

        /* change between login and signup forms */
        changeContext: function() {
            this.signingUp = !this.signingUp
            this.username = ''
            this.password = ''
            this.email = ''
            this.loginFailed = false
            this.passwordsDoNotMatch = false
            this.usernameTaken = false

            this.$nextTick(() => {
                this.$refs.username.focus()
            })
        }
    },
    mounted() {
        EventBus.$on('failedAuthentication', (msg) => {
            this.loginFailed = true
        })
    },
    beforeDestroy () {
        EventBus.$off('failedAuthentication')
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
    height: 25em;
}

.signup_main {
    height: 30em;
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

.errorText {
    display: block;
    padding-bottom: 1em;
}
</style>
