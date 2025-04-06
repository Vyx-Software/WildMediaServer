<template>
    <v-container>
      <!-- Libraries Section -->
      <v-row class="mb-8">
        <v-col cols="12">
          <h2 class="text-h4 mb-4">Your Libraries</h2>
          <v-progress-linear
            v-if="loadingLibraries"
            indeterminate
            color="primary"
          />
          <v-alert
            v-else-if="libraryError"
            type="error"
            variant="tonal"
          >
            {{ libraryError }}
          </v-alert>
          <v-row v-else>
            <v-col
              v-for="library in libraries"
              :key="library.id"
              cols="12"
              sm="6"
              md="4"
              lg="3"
            >
              <v-card
                :to="`/library/${library.id}`"
                height="200"
                class="library-card"
              >
                <v-img
                  :src="library.thumbnail || '/library-placeholder.jpg'"
                  height="100%"
                  cover
                  gradient="to bottom, rgba(0,0,0,0), rgba(0,0,0,0.7)"
                >
                  <v-card-title class="text-white">
                    {{ library.name }}
                  </v-card-title>
                  <v-card-subtitle class="text-white">
                    {{ library.mediaCount }} items
                  </v-card-subtitle>
                </v-img>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
  
      <!-- Recent Media Section -->
      <v-row>
        <v-col cols="12">
          <h2 class="text-h4 mb-4">Recently Added</h2>
          <v-progress-linear
            v-if="loadingRecent"
            indeterminate
            color="primary"
          />
          <v-alert
            v-else-if="recentError"
            type="error"
            variant="tonal"
          >
            {{ recentError }}
          </v-alert>
          <MediaGrid
            v-else
            :media-items="recentMedia"
            :items-per-page="8"
            class="recent-media-grid"
          />
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useStore } from 'vuex'
  import MediaGrid from '@/components/media/MediaGrid.vue'
  
  const store = useStore()
  
  const libraries = ref([])
  const recentMedia = ref([])
  const loadingLibraries = ref(true)
  const loadingRecent = ref(true)
  const libraryError = ref(null)
  const recentError = ref(null)
  
  onMounted(async () => {
    try {
      const [libResponse, recentResponse] = await Promise.all([
        store.dispatch('media/fetchLibraries'),
        store.dispatch('media/fetchRecentMedia')
      ])
      
      libraries.value = libResponse.data
      recentMedia.value = recentResponse.data
    } catch (err) {
      libraryError.value = 'Failed to load libraries: ' + err.message
      recentError.value = 'Failed to load recent media: ' + err.message
    } finally {
      loadingLibraries.value = false
      loadingRecent.value = false
    }
  })
  </script>
  
  <style scoped>
  .library-card {
    transition: transform 0.2s ease-in-out;
    cursor: pointer;
  }
  
  .library-card:hover {
    transform: translateY(-5px);
  }
  
  .recent-media-grid {
    border-radius: 8px;
    overflow: hidden;
  }
  </style>