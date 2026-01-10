import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface EditorTab {
    path: string
    name: string
    type: 'file' | 'directory'
    icon?: string
    isModified?: boolean
}

export const useEditorTabStore = defineStore('editorTab', () => {
    const tabs = ref<EditorTab[]>([])
    const activeTabPath = ref<string | null>(null)

    const activeTab = computed(() =>
        tabs.value.find(tab => tab.path === activeTabPath.value)
    )

    const openTab = (file: EditorTab) => {
        const existingTab = tabs.value.find(tab => tab.path === file.path)
        if (!existingTab) {
            tabs.value.push({ ...file, isModified: false })
        }
        activeTabPath.value = file.path
    }

    const closeTab = (path: string) => {
        const index = tabs.value.findIndex(tab => tab.path === path)
        if (index === -1) return

        // If closing the active tab, switch to another one
        if (activeTabPath.value === path) {
            if (tabs.value.length > 1) {
                // Try to go to the right, otherwise left
                const newIndex = index === tabs.value.length - 1 ? index - 1 : index + 1
                activeTabPath.value = tabs.value[newIndex].path
            } else {
                activeTabPath.value = null
            }
        }

        tabs.value.splice(index, 1)
    }

    const closeOtherTabs = (path: string) => {
        tabs.value = tabs.value.filter(tab => tab.path === path)
        activeTabPath.value = path
    }

    const closeAllTabs = () => {
        tabs.value = []
        activeTabPath.value = null
    }

    const setActiveTab = (path: string) => {
        if (tabs.value.find(tab => tab.path === path)) {
            activeTabPath.value = path
        }
    }

    const setTabModified = (path: string, modified: boolean) => {
        const tab = tabs.value.find(t => t.path === path)
        if (tab) {
            tab.isModified = modified
        }
    }

    return {
        tabs,
        activeTabPath,
        activeTab,
        openTab,
        closeTab,
        closeOtherTabs,
        closeAllTabs,
        setActiveTab,
        setTabModified
    }
})
