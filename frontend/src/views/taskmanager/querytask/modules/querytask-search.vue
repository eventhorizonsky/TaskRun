<template>
  <ArtSearchBar
    ref="searchBarRef"
    v-model="formData"
    :items="formItems"
    :rules="rules"
    @reset="handleReset"
    @search="handleSearch"
  >
  </ArtSearchBar>
</template>

<script setup lang="ts">
  interface Props {
    modelValue: Record<string, any>
  }
  interface Emits {
    (e: 'update:modelValue', value: Record<string, any>): void
    (e: 'search', params: Record<string, any>): void
    (e: 'reset'): void
  }
  const props = defineProps<Props>()
  const emit = defineEmits<Emits>()

  // 表单数据双向绑定
  const searchBarRef = ref()
  const formData = computed({
    get: () => props.modelValue,
    set: (val) => emit('update:modelValue', val)
  })

  // 校验规则
  const rules = {
    // task_id: [{ required: true, message: '请输入任务ID', trigger: 'blur' }]
  }

  // 动态 options
  const successOptions = ref<{ label: string; value: boolean }[]>([
    { label: '成功', value: true },
    { label: '失败', value: false }
  ])

  // 表单配置
  const formItems = computed(() => [
    {
      label: '任务ID',
      key: 'task_id',
      type: 'input',
      placeholder: '请输入任务ID',
      clearable: true
    },
    {
      label: '队列名称',
      key: 'queue_name',
      type: 'input',
      props: { placeholder: '请输入队列名称' }
    },
    {
      label: '成功状态',
      key: 'success',
      type: 'select',
      props: {
        placeholder: '请选择状态',
        options: successOptions.value
      }
    }
  ])

  // 事件
  function handleReset() {
    console.log('重置表单')
    emit('reset')
  }

  async function handleSearch() {
    await searchBarRef.value.validate()
    emit('search', formData.value)
    console.log('表单数据', formData.value)
  }
</script>