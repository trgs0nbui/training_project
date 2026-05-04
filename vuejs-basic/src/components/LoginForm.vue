<script setup>
import { ref } from 'vue'
import auth from '../stores/auth'

const email = ref('')
const password = ref('')

const handleLogin = () => {
    auth.login(email.value, password.value)
}
</script>

<template>

    <div>
        <h2>
            Login
        </h2>

        <input v-model="email" placeholder="Email"/>
        <input v-model="password" type="password" placeholder="Password"/>

        <button @click="handleLogin">
            Login
        </button>
    </div>
</template>