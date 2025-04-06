<template>
    <v-form @submit.prevent="handleSubmit">
      <v-card class="auth-card">
        <v-card-title class="text-h5 mb-4">
          Create Account
        </v-card-title>
  
        <v-card-text>
          <v-text-field
            v-model="form.username"
            label="Username"
            :rules="usernameRules"
            required
            variant="outlined"
          />
  
          <v-text-field
            v-model="form.email"
            label="Email"
            type="email"
            :rules="emailRules"
            required
            autocomplete="email"
            variant="outlined"
          />
  
          <v-text-field
            v-model="form.password"
            label="Password"
            type="password"
            :rules="passwordRules"
            required
            autocomplete="new-password"
            variant="outlined"
          />
  
          <v-text-field
            v-model="form.confirmPassword"
            label="Confirm Password"
            type="password"
            :rules="confirmPasswordRules"
            required
            variant="outlined"
          />
  
          <v-text-field
            v-model="form.inviteCode"
            label="Invite Code"
            :rules="inviteCodeRules"
            required
            variant="outlined"
            class="mb-4"
          />
  
          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            class="mb-4"
          >
            {{ errorMessage }}
          </v-alert>
  
          <v-btn
            type="submit"
            block
            size="large"
            color="primary"
            :loading="loading"
          >
            Create Account
          </v-btn>
  
          <v-divider class="my-4" />
  
          <div class="text-caption text-center">
            Already have an account? 
            <v-btn
              variant="text"
              color="primary"
              to="/login"
            >
              Sign In
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-form>
  </template>
  
  <script setup>
  import { reactive, ref, computed } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  
  const store = useStore()
  const router = useRouter()
  
  const form = reactive({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    inviteCode: ''
  })
  
  const loading = ref(false)
  const error = ref(false)
  const errorMessage = ref('')
  
  const usernameRules = [
    v => !!v || 'Username is required',
    v => v.length >= 3 || 'Username must be at least 3 characters'
  ]
  
  const emailRules = [
    v => !!v || 'Email is required',
    v => /.+@.+\..+/.test(v) || 'Email must be valid'
  ]
  
  const passwordRules = [
    v => !!v || 'Password is required',
    v => v.length >= 8 || 'Password must be at least 8 characters'
  ]
  
  const confirmPasswordRules = [
    v => !!v || 'Confirm Password is required',
    v => v === form.password || 'Passwords must match'
  ]
  
  const inviteCodeRules = [
    v => !!v || 'Invite code is required',
    v => v.length === 12 || 'Invalid invite code format'
  ]
  
  async function handleSubmit() {
    if (!validateForm()) return
  
    try {
      loading.value = true
      error.value = false
      
      await store.dispatch('auth/register', form)
      router.push('/login?registered=true')
    } catch (err) {
      error.value = true
      errorMessage.value = err.response?.data?.message || 'Registration failed. Please check your information.'
    } finally {
      loading.value = false
    }
  }
  
  function validateForm() {
    return usernameRules.every(rule => rule(form.username) === true) &&
           emailRules.every(rule => rule(form.email) === true) &&
           passwordRules.every(rule => rule(form.password) === true) &&
           confirmPasswordRules.every(rule => rule(form.confirmPassword) === true) &&
           inviteCodeRules.every(rule => rule(form.inviteCode) === true)
  }
  </script>
  
  <style scoped>
  .auth-card {
    max-width: 450px;
    margin: 0 auto;
    padding: 2rem;
    border-radius: 12px;
  }
  </style>