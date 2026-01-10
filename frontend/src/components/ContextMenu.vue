<template>
  <div
    v-show="visible"
    class="fixed z-50 bg-white dark:bg-[#252526] border border-gray-200 dark:border-[#454545] rounded shadow-lg py-1 min-w-[160px]"
    :style="{ left: x + 'px', top: y + 'px' }"
    @contextmenu.prevent
  >
    <div
      v-for="item in menuItems"
      :key="item.label"
      class="px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-100 dark:hover:bg-[#2a2d2e] flex items-center gap-2"
      :class="[
        item.danger ? 'text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20' : 'text-gray-700 dark:text-gray-300',
        item.disabled ? 'opacity-50 cursor-not-allowed hover:bg-transparent dark:hover:bg-transparent' : ''
      ]"
      @click="!item.disabled && handleClick(item)"
    >
      <component :is="item.icon" v-if="item.icon" class="w-4 h-4" />
      <span>{{ item.label }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { DocumentAdd, FolderAdd, Edit, Delete, Close, CloseBold } from '@element-plus/icons-vue'

interface MenuItem {
  label: string
  icon: any
  action: string
  show: boolean
  danger?: boolean
  disabled?: boolean
}

const props = defineProps<{
  visible: boolean
  x: number
  y: number
  targetNode: any
  menuType?: 'file' | 'tab'
}>()

const emit = defineEmits(['update:visible', 'select'])

const menuItems = computed<MenuItem[]>(() => {
  console.log('ContextMenu menuItems computed', {
    menuType: props.menuType,
    visible: props.visible,
    targetNode: props.targetNode
  })
  
  // Tab context menu
  if (props.menuType === 'tab') {
    const items = [
      { label: '关闭', icon: Close, action: 'close', show: true },
      { label: '关闭未修改', icon: Close, action: 'close-unmodified', show: true },
      { label: '关闭其他', icon: Close, action: 'close-others', show: true },
      { label: '关闭右侧', icon: Close, action: 'close-right', show: true },
      { label: '关闭左侧', icon: Close, action: 'close-left', show: true }
    ].filter(item => item.show)
    console.log('Tab menu items:', items)
    return items
  }
  
  // File tree context menu
  const isDir = props.targetNode?.data?.type === 'directory'
  
  return [
    { label: '新建文件', icon: DocumentAdd, action: 'new-file', show: isDir },
    { label: '新建文件夹', icon: FolderAdd, action: 'new-folder', show: isDir },
    { label: '重命名', icon: Edit, action: 'rename', show: true },
    { label: '删除', icon: Delete, action: 'delete', danger: true, show: true }
  ].filter(item => item.show)
})

const handleClick = (item: any) => {
  // For tab menu, pass the targetNode directly (it's the tab object)
  // For file tree menu, pass the targetNode (it's the tree node)
  emit('select', item.action, props.targetNode)
  emit('update:visible', false)
}

// Click outside to close
const closeMenu = (e: MouseEvent) => {
  emit('update:visible', false)
}

// Add event listeners only when menu becomes visible
// Remove them when menu is hidden
let listenersAdded = false

const addListeners = () => {
  if (!listenersAdded) {
    // Use setTimeout to avoid closing immediately due to the same event that opened the menu
    setTimeout(() => {
      document.addEventListener('click', closeMenu, { capture: true })
      document.addEventListener('contextmenu', closeMenu, { capture: true })
      listenersAdded = true
    }, 10)
  }
}

const removeListeners = () => {
  if (listenersAdded) {
    document.removeEventListener('click', closeMenu, { capture: true })
    document.removeEventListener('contextmenu', closeMenu, { capture: true })
    listenersAdded = false
  }
}

// Watch visibility changes
watch(() => props.visible, (newVal) => {
  if (newVal) {
    addListeners()
  } else {
    removeListeners()
  }
})

onUnmounted(() => {
  removeListeners()
})
</script>
