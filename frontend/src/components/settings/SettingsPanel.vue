<template>
    <v-container>
      <v-tabs v-model="tab" grow>
        <v-tab value="profile">Profile Settings</v-tab>
        <v-tab value="player">Player Settings</v-tab>
      </v-tabs>
  
      <v-window v-model="tab">
        <!-- Profile Settings -->
        <v-window-item value="profile">
          <v-form @submit.prevent="updateProfile">
            <v-card class="pa-6">
              <v-card-title class="text-h5 mb-4">Profile Settings</v-card-title>
              
              <v-text-field
                v-model="profileForm.email"
                label="Email"
                type="email"
                :rules="emailRules"
                required
                variant="outlined"
                class="mb-4"
              />
  
              <v-text-field
                v-model="profileForm.username"
                label="Username"
                :rules="usernameRules"
                variant="outlined"
                class="mb-4"
              />
  
              <v-file-input
                v-model="profileForm.avatar"
                label="Profile Picture"
                accept="image/*"
                prepend-icon="mdi-camera"
                variant="outlined"
                class="mb-4"
              />
  
              <v-btn
                type="submit"
                color="primary"
                :loading="updatingProfile"
              >
                Update Profile
              </v-btn>
            </v-card>
          </v-form>
  
          <v-divider class="my-8" />
  
          <v-card class="pa-6">
            <v-card-title class="text-h5 mb-4">Change Password</v-card-title>
            <v-form @submit.prevent="changePassword">
              <v-text-field
                v-model="passwordForm.currentPassword"
                label="Current Password"
                type="password"
                :rules="passwordRules"
                required
                variant="outlined"
                class="mb-4"
              />
  
              <v-text-field
                v-model="passwordForm.newPassword"
                label="New Password"
                type="password"
                :rules="passwordRules"
                required
                variant="outlined"
                class="mb-4"
              />
  
              <v-text-field
                v-model="passwordForm.confirmPassword"
                label="Confirm Password"
                type="password"
                :rules="confirmPasswordRules"
                required
                variant="outlined"
                class="mb-4"
              />
  
              <v-btn
                type="submit"
                color="primary"
                :loading="changingPassword"
              >
                Change Password
              </v-btn>
            </v-form>
          </v-card>
        </v-window-item>
  
        <!-- Player Settings -->
        <v-window-item value="player">
          <v-card class="pa-6">
            <v-card-title class="text-h5 mb-4">Player Preferences</v-card-title>
            
            <v-form @submit.prevent="savePlayerSettings">
              <v-select
                v-model="playerSettings.subtitleFont"
                :items="fontOptions"
                label="Subtitle Font"
                variant="outlined"
                class="mb-4"
              />
  
              <v-slider
                v-model="playerSettings.subtitleSize"
                label="Subtitle Size"
                min="12"
                max="48"
                step="2"
                thumb-label
                class="mb-4"
              />
  
              <v-color-picker
                v-model="playerSettings.subtitleColor"
                mode="hexa"
                label="Subtitle Color"
                class="mb-4"
              />
  
              <v-checkbox
                v-model="playerSettings.autoplayNext"
                label="Autoplay Next Episode"
                color="primary"
                class="mb-4"
              />
  
              <v-select
                v-model="playerSettings.defaultQuality"
                :items="qualityOptions"
                label="Default Video Quality"
                variant="outlined"
                class="mb-4"
              />
  
              <v-btn
                type="submit"
                color="primary"
                :loading="savingSettings"
              >
                Save Settings
              </v-btn>
            </v-form>
          </v-card>
        </v-window-item>
      </v-window>
    </v-container>
  </template>
  
  <script setup>
  import { ref, reactive, watchEffect } from 'vue'
  import { useStore } from 'vuex'
  
  const store = useStore()
  const tab = ref('profile')
  
  // Profile Settings
  const profileForm = reactive({
    email: '',
    username: '',
    avatar: null
  })
  
  const passwordForm = reactive({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
  
  // Player Settings
  const playerSettings = reactive({
    subtitleFont: 'Arial',
    subtitleSize: 24,
    subtitleColor: '#FFFFFF',
    autoplayNext: true,
    defaultQuality: '1080p'
  })
  
  const fontOptions = ['Arial', 'Helvetica', 'Verdana', 'Roboto']
  const qualityOptions = ['360p', '480p', '720p', '1080p', '4K']
  
  const updatingProfile = ref(false)
  const changingPassword = ref(false)
  const savingSettings = ref(false)
  
  // Validation Rules
  const emailRules = [
    v => !!v || 'Email is required',
    v => /.+@.+\..+/.test(v) || 'Email must be valid'
  ]
  
  const usernameRules = [
    v => !!v || 'Username is required',
    v => v.length >= 3 || 'Username must be at least 3 characters'
  ]
  
  const passwordRules = [
    v => !!v || 'Password is required',
    v => v.length >= 8 || 'Password must be at least 8 characters'
  ]
  
  const confirmPasswordRules = [
    v => !!v || 'Confirm Password is required',
    v => v === passwordForm.newPassword || 'Passwords must match'
  ]
  
  // Load initial settings
  watchEffect(async () => {
    const settings = await store.dispatch('user/fetchSettings')
    Object.assign(playerSettings, settings)
  })
  
  async function updateProfile() {
    updatingProfile.value = true
    try {
      await store.dispatch('user/updateProfile', profileForm)
      store.commit('showSnackbar', 'Profile updated successfully')
    } catch (error) {
      store.commit('showSnackbar', 'Error updating profile')
    } finally {
      updatingProfile.value = false
    }
  }
  
  async function changePassword() {
    changingPassword.value = true
    try {
      await store.dispatch('user/changePassword', passwordForm)
      store.commit('showSnackbar', 'Password changed successfully')
      Object.assign(passwordForm, {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      })
    } catch (error) {
      store.commit('showSnackbar', 'Error changing password')
    } finally {
      changingPassword.value = false
    }
  }
  
  async function savePlayerSettings() {
    savingSettings.value = true
    try {
      await store.dispatch('user/savePlayerSettings', playerSettings)
      store.commit('showSnackbar', 'Settings saved successfully')
    } catch (error) {
      store.commit('showSnackbar', 'Error saving settings')
    } finally {
      savingSettings.value = false
    }
  }
  </script>
  
  <style scoped>
  .v-color-picker {
    max-width: 300px;
  }
  </style>