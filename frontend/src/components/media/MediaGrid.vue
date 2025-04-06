<template>
    <div class="media-grid">
      <v-text-field
        v-model="searchQuery"
        label="Search media"
        outlined
        clearable
        prepend-inner-icon="mdi-magnify"
        class="mb-4"
      />
  
      <v-row>
        <v-col
          v-for="media in filteredMedia"
          :key="media.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="2"
        >
          <media-card 
            :media="media"
            @play="handlePlay"
            @click="navigateToMedia(media.id)"
          />
        </v-col>
      </v-row>
  
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        :total-visible="7"
        class="mt-4"
      />
    </div>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import MediaCard from './MediaCard.vue'
  
  const props = defineProps({
    mediaItems: {
      type: Array,
      required: true,
      default: () => []
    },
    itemsPerPage: {
      type: Number,
      default: 24
    }
  })
  
  const router = useRouter()
  const searchQuery = ref('')
  const currentPage = ref(1)
  
  const filteredMedia = computed(() => {
    return props.mediaItems.filter(media => {
      const query = searchQuery.value?.toLowerCase() || ''
      return media.title.toLowerCase().includes(query) ||
             media.metadata?.genre?.toLowerCase().includes(query)
    })
  })
  
  const totalPages = computed(() => {
    return Math.ceil(filteredMedia.value.length / props.itemsPerPage)
  })
  
  const paginatedMedia = computed(() => {
    const start = (currentPage.value - 1) * props.itemsPerPage
    const end = start + props.itemsPerPage
    return filteredMedia.value.slice(start, end)
  })
  
  function handlePlay(mediaId) {
    router.push({ name: 'Player', params: { id: mediaId } })
  }
  
  function navigateToMedia(mediaId) {
    router.push({ name: 'MediaDetail', params: { id: mediaId } })
  }
  </script>
  
  <style scoped>
  .media-grid {
    max-width: 1600px;
    margin: 0 auto;
    padding: 16px;
  }
  </style>