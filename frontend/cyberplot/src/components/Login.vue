<template>
<content>
    <VueTitle title="cyberplot" />

    <main>
        <form id="login_form">
            <img src="@/assets/images/logo_blue.svg" alt="Cyberplot logo">
            <input :class="{inputError: loginFailed || signupFailed}" type="text" ref="username" name="username" placeholder="Username" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_user_gray.svg')})`}" v-model="username" @focus="signupFailed = false" @keyup="clearLoginFailed" @keyup.enter="authenticate">
            <input :class="{inputError: loginFailed || passwordsDoNotMatch}" type="password" name="password" placeholder="Password" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_password_gray.svg')})`}" v-model="password" @keyup="clearLoginFailed" @focus="passwordsDoNotMatch = false" @blur="passwordsMatch" @keyup.enter="authenticate">
            <input v-if="signingUp" :class="{inputError: passwordsDoNotMatch}" type="password" name="password_confirm" placeholder="Confirm password" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_password_gray.svg')})`}" v-model="passwordConfirmation" @focus="passwordsDoNotMatch = false" @blur="passwordsMatch" @keyup.enter="authenticate">
            <input v-if="signingUp" :class="{inputError: invalidEmail}" type="email" name="email" placeholder="E-mail" class="textbox_with_icon" :style="{'background-image': `url(${require('@/assets/images/icon_email_gray.svg')})`}" v-model="email" @focus="invalidEmail = false" @blur="emailValid" @keyup.enter="authenticate">
            <span class="errorText" v-if="loginFailed">Incorrect username and/or password.</span>
            <span class="errorText" v-if="signupFailed">Username is already taken.</span>
            <span class="errorText" v-if="passwordsDoNotMatch">Passwords do not match.</span>
            <span class="errorText" v-if="invalidEmail">Invalid e-mail address.</span>
            <span class="infoText" v-if="accountCreated">Account created. Please log in.</span>
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
import VueTitle from './Helpers/Title.vue'

export default {
    name: 'Login',
    components: {
        VueTitle
    },
    data() {
        return {
            username: '',
            password: '',
            passwordConfirmation: '',
            email: '',
            loginFailed: false,
            signupFailed: false,
            passwordsDoNotMatch: false,
            invalidEmail: false,
            signingUp: false,
            accountCreated: false
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
                if(this.passwordsMatch() && this.emailValid()) {
                    this.$store.dispatch('signup', { username: this.username,
                                                     password: this.password,
                                                     email: this.email })
                        .then(() => { this.changeContext()
                                      this.accountCreated = true })
                }
            }
        },

        /* change between login and signup forms */
        changeContext: function() {
            this.signingUp = !this.signingUp
            this.username = ''
            this.password = ''
            this.passwordConfirmation = ''
            this.email = ''
            this.loginFailed = false
            this.signupFailed = false
            this.passwordsDoNotMatch = false
            this.invalidEmail = false
            this.accountCreated = false

            this.$nextTick(() => {
                this.$refs.username.focus()
            })
        },

        passwordsMatch: function() {
            if(this.signingUp) {
                let match = (this.password === this.passwordConfirmation)
                this.passwordsDoNotMatch = !match
                return match
            }
        },

        emailValid: function() {
            let re = /^([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x22([^\x0d\x22\x5c\x80-\xff]|\x5c[\x00-\x7f])*\x22))*\x40([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d)(\x2e([^\x00-\x20\x22\x28\x29\x2c\x2e\x3a-\x3c\x3e\x40\x5b-\x5d\x7f-\xff]+|\x5b([^\x0d\x5b-\x5d\x80-\xff]|\x5c[\x00-\x7f])*\x5d))*$/
            let valid = re.test(this.email)
            this.invalidEmail = !valid
            return valid
        },

        clearLoginFailed: function() {
            if(!this.signingUp) {
                this.loginFailed = false
            }
        }
    },
    mounted() {
        EventBus.$on('failedAuthentication', (msg) => {
            this.loginFailed = true
        })
        EventBus.$on('failedRegistering', (msg) => {
            this.signupFailed = true
        })
        this.$refs.username.focus()
    },
    beforeDestroy () {
        EventBus.$off('failedAuthentication')
        EventBus.$off('failedRegistering')
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
    height: auto;
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

.errorText, .infoText {
    display: block;
    padding-bottom: 1em;
}
</style>
