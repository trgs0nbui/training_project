<script setup>
    import { reactive } from 'vue';
    import auth from '../stores/auth';

    const form = reactive( {
        name: '',
        email: '',
        password: ''
    })

    const handleRegister = () => {
        auth.register(form)
    }
</script>

<template>
    <div>
        <h2>
            Register 
        </h2>
        <input v-model="form.name" placeholder="Name"/>
        <input v-model="form.email" placeholder="Email"/>
        <input v-model="form.password" placeholder="password"/>

        <button @click="handleRegister">
            Register
        </button>
    </div>
</template>