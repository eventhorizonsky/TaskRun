<!-- 工作台页面 -->
<template>
  <div class="console-page art-full-height">
    <!-- <CardList></CardList>

    <ElRow :gutter="20">
      <ElCol :sm="24" :md="12" :lg="10">
        <ActiveUser />
      </ElCol>
      <ElCol :sm="24" :md="12" :lg="14">
        <SalesOverview />
      </ElCol>
    </ElRow> -->

    <ElRow :gutter="20">
      <ElCol :sm="24" :md="24" :lg="24">
        <ProcessManagement />
      </ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :sm="24" :md="24" :lg="24">
        <QueueRunInfo />
      </ElCol>
    </ElRow>

    <!-- <ElRow :gutter="20">
      <ElCol :sm="24" :md="12" :lg="6">
        <Dynamic />
      </ElCol>
      <ElCol :sm="24" :md="12" :lg="6">
        <TodoList />
      </ElCol>
    </ElRow> -->

    <!-- <AboutProject /> -->
  </div>
</template>

<script setup lang="ts">
  import QueueRunInfo from './modules/queue-run-info.vue'
  import ProcessManagement from './modules/process-management.vue'

  defineOptions({ name: 'Console' })
</script>
