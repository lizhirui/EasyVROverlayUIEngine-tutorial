<script setup lang="ts">
import { computed, shallowRef } from 'vue'
import { onContentUpdated, useData } from 'vitepress'
import type { DefaultTheme } from 'vitepress'
import VPSidebarGroup from 'vitepress/dist/client/theme-default/components/VPSidebarGroup.vue'
import VPDocOutlineItem from 'vitepress/dist/client/theme-default/components/VPDocOutlineItem.vue'
import { getHeaders } from 'vitepress/dist/client/theme-default/composables/outline.js'
import { useSidebar } from 'vitepress/dist/client/theme-default/composables/sidebar.js'
import DocDrawer from './DocDrawer.vue'

const { lang, theme, frontmatter } = useData<DefaultTheme.Config>()
const { hasSidebar, hasAside, sidebarGroups } = useSidebar()
const headerList = shallowRef<ReturnType<typeof getHeaders>>([])

const labelMap = {
  zh: { menu: '章节目录', outline: '本页大纲', open: '打开', close: '关闭' },
  en: { menu: 'Chapters', outline: 'On this page', open: 'Open ', close: 'Close ' },
  ja: { menu: '章一覧', outline: 'このページの目次', open: 'を開く', close: 'を閉じる' }
}

const locale = computed(() => lang.value.startsWith('ja') ? 'ja' : lang.value.startsWith('en') ? 'en' : 'zh')
const label = computed(() => labelMap[locale.value])

function describeAction(action: 'open' | 'close', title: string) {
  return locale.value === 'ja' ? title + label.value[action] : label.value[action] + title
}

onContentUpdated(() => {
  headerList.value = hasAside.value ? getHeaders(frontmatter.value.outline ?? theme.value.outline) : []
})
</script>

<template>
  <div class="tutorial-toolbar" v-if="hasSidebar || headerList.length">
    <DocDrawer
      v-if="hasSidebar"
      id="tutorial-chapters"
      side="left"
      :label="label.menu"
      :open-label="describeAction('open', label.menu)"
      :close-label="describeAction('close', label.menu)"
    >
      <nav :aria-label="label.menu">
        <VPSidebarGroup :items="sidebarGroups" />
      </nav>
    </DocDrawer>
    <DocDrawer
      v-if="headerList.length"
      id="tutorial-outline"
      side="right"
      :label="label.outline"
      :open-label="describeAction('open', label.outline)"
      :close-label="describeAction('close', label.outline)"
    >
      <nav :aria-label="label.outline">
        <VPDocOutlineItem :headers="headerList" root />
      </nav>
    </DocDrawer>
  </div>
</template>
