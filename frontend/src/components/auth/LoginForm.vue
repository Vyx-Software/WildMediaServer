<template>
    <v-form @submit.prevent="handleSubmit">
      <v-card class="auth-card">
        <v-card-title class="text-h5 mb-4">
          Welcome to WildMedia
        </v-card-title>
  
        <v-card-text>
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
            autocomplete="current-password"
            variant="outlined"
          />
  
          <div class="d-flex justify-space-between align-center mt-2">
            <v-checkbox
              v-model="form.rememberMe"
              label="Remember me"
              density="comfortable"
            />
            <v-btn
              variant="text"
              color="primary"
              to="/forgot-password"
            >
              Forgot Password?
            </v-btn>
          </div>
  
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
            Sign In
          </v-btn>
  
          <v-divider class="my-4" />
  
          <div class="social-logins">
            <v-btn
              block
              variant="outlined"
              color="grey-darken-2"
              class="mb-2"
              @click="signInWithGoogle"
            >
              <v-icon left>mdi-google</v-icon>
              Continue with Google
            </v-btn>
  
            <v-btn
              block
              variant="outlined"
              color="grey-darken-2"
              @click="signInWithGitHub"
            >
              <v-icon left>mdi-github</v-icon>
              Continue with GitHub
            </v-btn>
          </div>
        </v-card-text>
  
        <v-card-actions class="justify-center">
          <span class="text-caption">
            Don't have an account? 
            <v-btn
              variant="text"
              color="primary"
              to="/register"
            >
              Sign Up
            </v-btn>
          </span>
        </v-card-actions>
      </v-card>
    </v-form>
  </template>
  
  <script setup>
  import { reactive, ref } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  
  const store = useStore()
  const router = useRouter()
  
  const form = reactive({
    email: '',
    password: '',
    rememberMe: false
  })
  
  const loading = ref(false)
  const error = ref(false)
  const errorMessage = ref('')
  
  const emailRules = [
    v => !!v || 'Email is required',
    v => /.+@.+\..+/.test(v) || 'Email must be valid'
  ]
  
  const passwordRules = [
    v => !!v || 'Password is required',
    v => v.length >= 8 || 'Password must be at least 8 characters'
  ]
  
  async function handleSubmit() {
    if (!validateForm()) return
  
    try {
      loading.value = true
      error.value = false
      
      await store.dispatch('auth/login', {
        email: form.email,
        password: form.password,
        rememberMe: form.rememberMe
      })
      
      router.push(store.state.auth.redirectRoute || '/')
    } catch (err) {
      error.value = true
      errorMessage.value = err.response?.data?.message || 'Login failed. Please check your credentials.'
    } finally {
      loading.value = false
    }
  }
  
  function validateForm() {
    return emailRules.every(rule => rule(form.email) === true) &&
           passwordRules.every(rule => rule(form.password) === true)
  }
  
  function signInWithGoogle() {
    // Implement OAuth2 integration
  }
  
  function signInWithGitHub() {
    // Implement OAuth2 integration
  }
  </script>
  
  <style scoped>
  .auth-card {
    max-width: 450px;
    margin: 0 auto;
    padding: 2rem;
    border-radius: 12px;
  }
  
  .social-logins {
    margin-top: 1.5rem;
  }
  </style>