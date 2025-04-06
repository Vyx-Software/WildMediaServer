<template>
    <v-app-bar
      app
      :color="$vuetify.theme.current.dark ? 'background' : 'surface'"
      :elevation="scrollY > 0 ? 4 : 0"
      :class="{ 'scrolled': scrollY > 0 }"
    >
      <v-app-bar-nav-icon @click="toggleDrawer" />
      
      <v-toolbar-title class="d-flex align-center">
        <v-img
          :src="logo"
          alt="WildTV Logo"
          max-width="120"
          contain
          class="mr-2"
        />
      </v-toolbar-title>
  
      <v-spacer />
  
      <v-btn
        v-for="item in visibleNavItems"
        :key="item.title"
        text
        :to="item.to"
        active-class="active-nav-item"
      >
        <v-icon left>{{ item.icon }}</v-icon>
        {{ item.title }}
      </v-btn>
  
      <v-menu offset-y transition="slide-y-transition">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar size="36">
              <v-img
                v-if="user?.profile_icon"
                :src="user.profile_icon"
                alt="Profile"
              />
              <v-icon v-else>mdi-account-circle</v-icon>
            </v-avatar>
          </v-btn>
        </template>
  
        <v-list nav>
          <v-list-item v-if="isAuthenticated" @click="navigateToProfile">
            <v-list-item-title>Profile Settings</v-list-item-title>
          </v-list-item>
          <v-list-item @click="toggleTheme">
            <v-list-item-title>
              {{ darkMode ? 'Light Mode' : 'Dark Mode' }}
            </v-list-item-title>
          </v-list-item>
          <v-divider />
          <v-list-item @click="handleAuthAction">
            <v-list-item-title>
              {{ isAuthenticated ? 'Logout' : 'Login' }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  </template>
  
  <script setup>
  import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
  import { useRouter } from 'vue-router'
  import { useStore } from 'vuex'
  import logo from '@/assets/logos/wildtv-logo.svg'
  
  const store = useStore()
  const router = useRouter()
  const scrollY = ref(0)
  
  const navItems = [
    { title: 'Home', to: '/', icon: 'mdi-home', auth: false },
    { title: 'Libraries', to: '/libraries', icon: 'mdi-library-movie', auth: true },
    { title: 'Admin', to: '/admin', icon: 'mdi-shield-account', auth: true, admin: true }
  ]
  
  const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
  const user = computed(() => store.getters['auth/currentUser'])
  const darkMode = computed(() => store.state.settings.darkMode)
  
  const visibleNavItems = computed(() => {
    return navItems.filter(item => {
      if (item.admin && !user.value?.isAdmin) return false
      return !item.auth || (item.auth && isAuthenticated.value)
    })
  })
  
  function handleScroll() {
    scrollY.value = window.scrollY
  }
  
  function toggleDrawer() {
    store.commit('ui/toggleDrawer')
  }
  
  function toggleTheme() {
    store.dispatch('settings/toggleDarkMode')
  }
  
  function navigateToProfile() {
    router.push('/settings/profile')
  }
  
  async function handleAuthAction() {
    if (isAuthenticated.value) {
      await store.dispatch('auth/logout')
      router.push('/login')
    } else {
      router.push('/login')
    }
  }
  
  onMounted(() => {
    window.addEventListener('scroll', handleScroll)
  })
  
  onBeforeUnmount(() => {
    window.removeEventListener('scroll', handleScroll)
  })
  </script>
  
  <style scoped>
  .scrolled {
    backdrop-filter: blur(8px);
    background-color: rgba(var(--v-theme-surface), 0.85) !important;
  }
  
  .active-nav-item {
    color: rgb(var(--v-theme-primary)) !important;
    font-weight: 600;
  }
  
  .v-app-bar {
    transition: background-color 0.3s ease, backdrop-filter 0.3s ease;
  }
  </style>