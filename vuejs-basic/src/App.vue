<script setup>
import auth from './stores/auth';
import LoginForm from './components/LoginForm.vue';
import RegisterForm from './components/RegisterForm.vue';
import UserInfo from './components/UserInfo.vue';
</script>

<template>
  <div>
    <h1>Ecommerce Auth</h1>
    <div v-if="!auth.isAuthenticated.value">
      <LoginForm/>
      <RegisterForm/>
    </div>

    <div v-else>
      <UserInfo/>
    </div>
  </div>
</template>
