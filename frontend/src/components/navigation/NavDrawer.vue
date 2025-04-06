<template>
    <v-navigation-drawer
      v-model="drawerOpen"
      app
      temporary
      :permanent="$vuetify.display.mdAndUp"
      :width="280"
    >
      <v-list nav>
        <v-list-item
          v-for="item in visibleNavItems"
          :key="item.title"
          :to="item.to"
          active-class="active-nav-item"
        >
          <template v-slot:prepend>
            <v-icon>{{ item.icon }}</v-icon>
          </template>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
  
      <template v-slot:append>
        <div class="pa-4">
          <v-btn
            block
            variant="outlined"
            @click="toggleTheme"
          >
            <v-icon left>
              {{ darkMode ? 'mdi-weather-sunny' : 'mdi-weather-night' }}
            </v-icon>
            {{ darkMode ? 'Light Mode' : 'Dark Mode' }}
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { useStore } from 'vuex'
  
  const store = useStore()
  
  const drawerOpen = computed({
    get: () => store.state.ui.drawerOpen,
    set: (value) => store.commit('ui/setDrawerOpen', value)
  })
  
  const darkMode = computed(() => store.state.settings.darkMode)
  const navItems = computed(() => store.getters['navigation/visibleNavItems'])
  
  function toggleTheme() {
    store.dispatch('settings/toggleDarkMode')
  }
  </script>