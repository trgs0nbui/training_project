import { ref, computed, watch } from 'vue'

// state
const user = ref(
  JSON.parse(localStorage.getItem('user')) || null
)
// computed
const isAuthenticated = computed(() => {
  return user.value && user.value.email
})

// login
const login = (email, password) => {
    // fake login
    if(email === 'admin@gmail.com' && password === '123456') {
        user.value = {
            email,
            name: 'Admin'
        }
    } else {
        alert('Invalid credentials')
    }
}

// register
const register = (data) => {
    user.value = data
}

// logout
const logout = () => {
    user.value = null
}

// persist (watch)
watch(user, (newUser) => {
    if (newUser) {
        localStorage.setItem('user', JSON.stringify(newUser))
    } else {
        localStorage.removeItem('user')
    }
}, { deep: true })

export default {
    user,
    isAuthenticated,
    login,
    register,
    logout
}