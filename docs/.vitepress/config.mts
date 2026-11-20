import { defineConfig } from 'vitepress'
import { existsSync } from 'node:fs'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { zh } from './locales/zh.mts'
import { en } from './locales/en.mts'
import { ja } from './locales/ja.mts'

const docsBase = process.env.DOCS_BASE || '/'

export default withMermaid(
  defineConfig({
    base: docsBase,
    title: 'EasyVROverlayUIEngine',
    cleanUrls: true,
    lastUpdated: true,
    markdown: {
      config(markdown) {
        const renderCode = markdown.renderer.rules.code_inline!
        markdown.renderer.rules.code_inline = (tokenList, index, options, environment, renderer) => {
          const token = tokenList[index]
          if (token.content.includes('{{')) {
            token.attrSet('v-pre', '')
          }
          return renderCode(tokenList, index, options, environment, renderer)
        }
      }
    },
    transformPageData(page) {
      const localPath = page.relativePath.replace(/^(en|ja)\//, '')
      page.frontmatter.availableLocaleList = ['root', 'en', 'ja'].filter(key => {
        const localePath = key === 'root' ? localPath : key + '/' + localPath
        return existsSync(new URL('../' + localePath, import.meta.url))
      })
    },
    head: [
      ['meta', { name: 'theme-color', content: '#3b82f6' }]
    ],
    themeConfig: {
      i18nRouting: false,
      search: {
        provider: 'local',
        options: {
          locales: {
            root: {
              translations: {
                button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
                modal: {
                  noResultsText: '没有找到相关内容',
                  resetButtonTitle: '清空查询',
                  footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
                }
              }
            },
            en: {
              translations: {
                button: { buttonText: 'Search', buttonAriaLabel: 'Search docs' },
                modal: {
                  noResultsText: 'No matching results',
                  resetButtonTitle: 'Clear query',
                  footer: { selectText: 'to select', navigateText: 'to navigate', closeText: 'to close' }
                }
              }
            },
            ja: {
              translations: {
                button: { buttonText: '検索', buttonAriaLabel: 'ドキュメントを検索' },
                modal: {
                  noResultsText: '一致する結果が見つかりません',
                  resetButtonTitle: 'クリア',
                  footer: { selectText: '選択', navigateText: '移動', closeText: '閉じる' }
                }
              }
            }
          }
        }
      }
    },
    locales: {
      root: zh,
      en,
      ja
    },
    mermaid: {
      theme: 'neutral'
    }
  })
)
