<script setup>
    import auth from '../stores/auth';
</script>

<template>
    <div>
        <h2 v-if="auth.isAuthenticated">
            Welcome {{ auth.user?.name }}
        </h2>

        <button v-if="auth.isAuthenticated" @click="auth.logout">
            Logout
        </button>
    </div>
</template>