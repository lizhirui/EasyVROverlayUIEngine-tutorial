<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useData, useRoute, withBase } from 'vitepress'

defineProps<{ mobile?: boolean }>()

const { localeIndex, page, site } = useData()
const route = useRoute()
const picker = ref<HTMLDetailsElement>()
const trigger = ref<HTMLElement>()
const localeOrder = ['root', 'en', 'ja'] as const
const actionLabel = {
  root: '切换语言',
  en: 'Change language',
  ja: '言語を切り替える'
}

const label = computed(() => actionLabel[localeIndex.value as keyof typeof actionLabel] ?? actionLabel.root)
const documentPath = computed(() => {
  const path = page.value.isNotFound ? 'index.md' : page.value.relativePath
  const localePrefix = localeIndex.value + '/'
  const localPath = localeIndex.value !== 'root' && path.startsWith(localePrefix)
    ? path.slice(localePrefix.length)
    : path

  return localPath.replace(/(^|\/)index\.md$/, '$1').replace(/\.md$/, site.value.cleanUrls ? '' : '.html')
})

const languageList = computed(() => localeOrder.map(key => {
  const locale = site.value.locales[key]
  const prefix = locale.link ?? (key === 'root' ? '/' : '/' + key + '/')
  const availableLocaleList = page.value.frontmatter.availableLocaleList as string[] | undefined
  const targetPath = !availableLocaleList || availableLocaleList.includes(key) ? documentPath.value : ''

  return {
    key,
    label: locale.label,
    lang: locale.lang,
    href: withBase(prefix.replace(/\/$/, '') + '/' + targetPath)
  }
}))

function closePicker() {
  if (picker.value) {
    picker.value.open = false
  }
}

function closeOnEscape(event: KeyboardEvent) {
  if (picker.value?.open) {
    event.preventDefault()
    event.stopPropagation()
    closePicker()
    trigger.value?.focus()
  }
}

function closeOnFocusOut(event: FocusEvent) {
  if (event.relatedTarget instanceof Node && !picker.value?.contains(event.relatedTarget)) {
    closePicker()
  }
}

function closeOnOutsideClick(event: PointerEvent) {
  if (picker.value?.open && event.target instanceof Node && !picker.value.contains(event.target)) {
    closePicker()
  }
}

watch(() => route.path, closePicker)
onMounted(() => document.addEventListener('pointerdown', closeOnOutsideClick))
onUnmounted(() => document.removeEventListener('pointerdown', closeOnOutsideClick))
</script>

<template>
  <details
    ref="picker"
    class="tutorial-locale-picker"
    :class="{ 'is-mobile': mobile }"
    @keydown.esc="closeOnEscape"
    @focusout="closeOnFocusOut"
  >
    <summary ref="trigger" :aria-label="label" :title="label">
      <span class="vpi-languages" aria-hidden="true" />
      <span v-if="mobile">{{ label }}</span>
      <span class="vpi-chevron-down tutorial-locale-chevron" aria-hidden="true" />
    </summary>

    <ul class="tutorial-locale-list" :aria-label="label">
      <li v-for="language in languageList" :key="language.key">
        <span
          v-if="language.key === localeIndex"
          class="tutorial-locale-option is-current"
          :lang="language.lang"
          aria-current="page"
        >
          {{ language.label }}
          <span aria-hidden="true">✓</span>
        </span>
        <a v-else class="tutorial-locale-option" :href="language.href" :lang="language.lang">
          {{ language.label }}
        </a>
      </li>
    </ul>
  </details>
</template>
