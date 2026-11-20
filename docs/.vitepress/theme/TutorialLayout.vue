<script setup lang="ts">
import { computed } from 'vue'
import { useData } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import DocNavigation from './DocNavigation.vue'
import LocalePicker from './LocalePicker.vue'

const { frontmatter, page } = useData()
const isDoc = computed(() =>
  !page.value.isNotFound && (frontmatter.value.layout == null || frontmatter.value.layout === 'doc')
)
</script>

<template>
  <div class="tutorial-site" :class="{ 'tutorial-doc-shell': isDoc }">
    <DefaultTheme.Layout>
      <template #nav-bar-content-after>
        <LocalePicker />
      </template>
      <template #nav-screen-content-after>
        <LocalePicker mobile />
      </template>
      <template #doc-top>
        <DocNavigation v-if="isDoc" />
      </template>
    </DefaultTheme.Layout>
  </div>
</template>
