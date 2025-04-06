<template>
    <div class="media-player">
      <div v-if="loading" class="text-center">
        <v-progress-circular indeterminate size="64" />
      </div>
  
      <template v-else>
        <video-player 
          ref="player"
          :options="playerOptions"
          @ready="setupPlayer"
          @error="handlePlayerError"
        />
  
        <div class="player-controls">
          <v-select
            v-model="selectedSubtitle"
            :items="availableSubtitles"
            label="Subtitles"
            outlined
            dense
            class="subtitle-select"
          />
  
          <div class="related-content">
            <h3 class="mb-4">Related Content</h3>
            <media-grid :media-items="relatedMedia" />
          </div>
        </div>
      </template>
  
      <v-alert
        v-if="error"
        type="error"
        dismissible
        class="mt-4"
      >
        {{ errorMessage }}
      </v-alert>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch, onBeforeUnmount } from 'vue'
  import { useRoute } from 'vue-router'
  import { useStore } from 'vuex'
  import VideoPlayer from 'vue-video-player'
  
  const props = defineProps({
    mediaId: {
      type: [String, Number],
      required: true
    }
  })
  
  const store = useStore()
  const route = useRoute()
  const player = ref(null)
  const loading = ref(true)
  const error = ref(null)
  const selectedSubtitle = ref(null)
  
  const media = computed(() => {
    return store.getters['media/getMediaById'](props.mediaId)
  })
  
  const relatedMedia = computed(() => {
    return store.getters['media/getRelatedMedia'](props.mediaId)
  })
  
  const availableSubtitles = computed(() => {
    return media.value?.subtitles?.map(sub => ({
      text: sub.language.toUpperCase(),
      value: sub.url
    })) || []
  })
  
  const playerOptions = computed(() => ({
    autoplay: false,
    controls: true,
    responsive: true,
    fluid: true,
    sources: [{
      src: media.value.streamUrl,
      type: 'video/mp4'
    }],
    tracks: selectedSubtitle.value ? [{
      kind: 'subtitles',
      src: selectedSubtitle.value,
      srclang: 'en',
      label: 'English'
    }] : []
  }))
  
  async function loadMedia() {
    try {
      loading.value = true
      await store.dispatch('media/fetchMediaDetails', props.mediaId)
      error.value = null
    } catch (err) {
      error.value = true
    } finally {
      loading.value = false
    }
  }
  
  function setupPlayer(player) {
    player.on('ended', handlePlaybackEnded)
    player.on('timeupdate', handleTimeUpdate)
  }
  
  function handlePlayerError(error) {
    console.error('Player error:', error)
    error.value = 'Failed to load media playback'
  }
  
  function handlePlaybackEnded() {
    store.dispatch('user/logPlayback', {
      mediaId: props.mediaId,
      duration: media.value.metadata.duration
    })
  }
  
  function handleTimeUpdate(time) {
    store.dispatch('user/updatePlaybackProgress', {
      mediaId: props.mediaId,
      time: time
    })
  }
  
  watch(() => props.mediaId, loadMedia, { immediate: true })
  
  onBeforeUnmount(() => {
    if (player.value) {
      player.value.dispose()
    }
  })
  </script>
  
  <style scoped>
  .media-player {
    max-width: 1600px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .player-controls {
    margin-top: 24px;
  }
  
  .subtitle-select {
    max-width: 200px;
  }
  
  .related-content {
    margin-top: 32px;
  }
  </style>