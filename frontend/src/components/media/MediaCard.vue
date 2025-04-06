<template>
    <v-card 
      class="media-card"
      :elevation="hover ? 6 : 2"
      @mouseover="hover = true"
      @mouseleave="hover = false"
      @click="handleClick"
    >
      <v-img
        :src="thumbnail"
        :alt="media.title"
        height="200"
        cover
        gradient="to bottom, rgba(0,0,0,0), rgba(0,0,0,0.7)"
      >
        <v-card-title class="media-title">
          {{ media.title }}
        </v-card-title>
        
        <template v-slot:placeholder>
          <v-skeleton-loader type="image" />
        </template>
      </v-img>
  
      <v-card-subtitle class="d-flex align-center">
        <v-chip 
          small 
          :color="mediaTypeColor"
          class="mr-2"
        >
          {{ mediaTypeLabel }}
        </v-chip>
        <span class="text-caption">{{ formattedDuration }}</span>
      </v-card-subtitle>
  
      <v-card-actions>
        <v-btn 
          icon
          @click.stop="toggleFavorite"
        >
          <v-icon :color="isFavorite ? 'red' : 'grey'">
            {{ isFavorite ? 'mdi-heart' : 'mdi-heart-outline' }}
          </v-icon>
        </v-btn>
        <v-spacer />
        <v-btn 
          color="primary"
          small
          @click.stop="emitPlay"
        >
          Play
        </v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue'
  import { useStore } from 'vuex'
  import { durationFormatter } from '@/utils/helpers'
  
  const props = defineProps({
    media: {
      type: Object,
      required: true,
      validator: value => {
        return ['id', 'title', 'type', 'metadata'].every(key => key in value)
      }
    }
  })
  
  const emit = defineEmits(['play', 'click'])
  
  const store = useStore()
  const hover = ref(false)
  
  const thumbnail = computed(() => {
    return props.media.metadata?.thumbnail || '/placeholder.jpg'
  })
  
  const mediaTypeColor = computed(() => {
    return props.media.type === 'movie' ? 'primary' : 'secondary'
  })
  
  const mediaTypeLabel = computed(() => {
    return props.media.type?.toUpperCase() || 'MEDIA'
  })
  
  const formattedDuration = computed(() => {
    return durationFormatter(props.media.metadata?.duration)
  })
  
  const isFavorite = computed(() => {
    return store.getters['user/isFavoriteMedia'](props.media.id)
  })
  
  function toggleFavorite() {
    store.dispatch('user/toggleFavorite', props.media.id)
  }
  
  function emitPlay() {
    emit('play', props.media.id)
  }
  
  function handleClick() {
    emit('click', props.media.id)
  }
  </script>
  
  <style scoped>
  .media-card {
    transition: transform 0.2s ease-in-out;
    cursor: pointer;
  }
  
  .media-card:hover {
    transform: translateY(-4px);
  }
  
  .media-title {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    color: white;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  }
  </style>