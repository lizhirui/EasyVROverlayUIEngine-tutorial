<script setup lang="ts">
import { ref, watch } from 'vue'
import { useData, useRoute } from 'vitepress'

defineProps<{
  id: string
  side: 'left' | 'right'
  label: string
  openLabel: string
  closeLabel: string
}>()

const panel = ref<HTMLDialogElement>()
const opened = ref(false)
const route = useRoute()
const { hash } = useData()

function openDrawer() {
  if (panel.value && !panel.value.open) {
    panel.value.showModal()
    opened.value = true
  }
}

function closeDrawer() {
  panel.value?.close()
}

function closeOnLink(event: MouseEvent) {
  if (event.target instanceof Element && event.target.closest('a[href]')) {
    closeDrawer()
  }
}

watch([() => route.path, hash], closeDrawer)
</script>

<template>
  <button
    type="button"
    class="tutorial-drawer-toggle"
    :class="side"
    :aria-controls="id"
    :aria-expanded="opened"
    aria-haspopup="dialog"
    :aria-label="openLabel"
    :title="openLabel"
    @click="openDrawer"
  >
    <span class="vpi-align-left tutorial-drawer-icon" aria-hidden="true" />
    {{ label }}
  </button>

  <dialog
    ref="panel"
    :id="id"
    class="tutorial-drawer"
    :class="side"
    :aria-labelledby="id + '-label'"
    @close="opened = false"
    @click.self="closeDrawer"
    @click.capture="closeOnLink"
  >
    <header class="tutorial-drawer-header">
      <div :id="id + '-label'" class="tutorial-drawer-title" role="heading" aria-level="2">{{ label }}</div>
      <button
        type="button"
        class="tutorial-drawer-close"
        :aria-label="closeLabel"
        :title="closeLabel"
        autofocus
        @click="closeDrawer"
      >
        <span aria-hidden="true">×</span>
      </button>
    </header>
    <div class="tutorial-drawer-content">
      <slot />
    </div>
  </dialog>
</template>
