<template>
  <div>
    <ElRow :gutter="20" class="flex mb-5">
      <ElCol v-for="(item, index) in cardDataList" :key="index" :sm="12" :md="6" :lg="6">
        <div class="art-card relative flex flex-col justify-center h-35 px-5 mb-5 max-sm:mb-4">
          <span class="text-g-700 text-sm">{{ item.des }}</span>
          <ArtCountTo class="text-[26px] font-medium mt-2" :target="item.num" :duration="1300" />
          <div
            class="absolute top-0 bottom-0 right-5 m-auto size-12.5 rounded-xl flex-cc bg-theme/10"
          >
            <ArtSvgIcon :icon="item.icon" class="text-xl text-theme" />
          </div>
        </div>
      </ElCol>
    </ElRow>

    <div class="art-card p-4 box-border">
      <h3 class="text-lg font-medium mb-4">队列详情</h3>
      <div class="space-y-3 max-h-96 overflow-y-auto">
        <div v-for="(queue, queueName) in queues" :key="queueName" class="art-card p-3 cursor-pointer" @click="handleQueueClick(queueName)">
          <div class="flex justify-between items-center mb-2">
            <span class="font-medium text-base">{{ queueName }}</span>
            <ElTag :type="queue.pause_flag === 0 ? 'success' : 'danger'" size="small">
              {{ queue.pause_flag === 0 ? '运行中' : '已暂停' }}
            </ElTag>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
            <div>
              <span class="text-g-500">消费成功次数:</span>
              <span class="font-medium">{{ queue.active_consumers.length }}</span>
            </div>
            <div>
              <span class="text-g-500">消息数量:</span>
              <span class="font-medium">{{ queue.msg_num_in_broker }}</span>
            </div>
            <div>
              <span class="text-g-500">总执行次数:</span>
              <span class="font-medium">{{ queue.all_consumers_total_consume_count_from_start }}</span>
            </div>
            <div>
              <span class="text-g-500">失败次数:</span>
              <span class="font-medium">{{ queue.all_consumers_total_consume_count_from_start_fail }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, reactive, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { fetchGetAllQueueRunInfo } from '@/api/funboost'

  const router = useRouter()

  interface CardDataItem {
    des: string
    icon: string
    startVal: number
    duration: number
    num: number
    change: string
  }

  const queues = ref<Record<string, Api.Funboost.QueueParamsAndActiveConsumersData>>({})
  const totalQueues = ref(0)

  const cardDataList = reactive<CardDataItem[]>([
    {
      des: '总队列数',
      icon: 'material-symbols-light:featured-play-list-outline',
      startVal: 0,
      duration: 1000,
      num: 0,
      change: '+0%'
    },
    {
      des: '活跃队列',
      icon: 'ic:sharp-online-prediction',
      startVal: 0,
      duration: 1000,
      num: 0,
      change: '+0%'
    },
    {
      des: '消费次数',
      icon: 'ri:group-line',
      startVal: 0,
      duration: 1000,
      num: 0,
      change: '+0%'
    },
    {
      des: '待执行消息数',
      icon: 'ri:mail-line',
      startVal: 0,
      duration: 1000,
      num: 0,
      change: '+0%'
    }
  ])

  const loadQueueRunInfo = async () => {
    try {
      const data = await fetchGetAllQueueRunInfo()
      if (data) {
        queues.value = data.queues
        totalQueues.value = data.total_count

        // 计算统计数据
        const activeQueues = Object.values(data.queues).filter(q => q.pause_flag === 0).length
        const totalConsumers = Object.values(data.queues).reduce((sum, q) => sum + q.active_consumers.length, 0)
        const totalMessages = Object.values(data.queues).reduce((sum, q) => sum + q.msg_num_in_broker, 0)

        cardDataList[0].num = totalQueues.value
        cardDataList[1].num = activeQueues
        cardDataList[2].num = totalConsumers
        cardDataList[3].num = totalMessages

        // 这里可以根据实际需求计算变化百分比
        // 暂时设置为+0%，实际项目中可能需要从缓存或历史数据计算
      }
    } catch (error) {
      console.error('Failed to load queue run info:', error)
    }
  }

  const handleQueueClick = (queueName: string) => {
    router.push({ path: '/taskmanager/querytask', query: { queue_name: queueName } })
  }

  onMounted(() => {
    loadQueueRunInfo()
  })
</script>