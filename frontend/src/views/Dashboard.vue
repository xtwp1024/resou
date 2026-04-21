<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #409eff">
              <el-icon :size="30"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_stars || 0 }}</div>
              <div class="stat-label">明星总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #67c23a">
              <el-icon :size="30"><Star /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.by_level?.顶流 || 0 }}</div>
              <div class="stat-label">顶流明星</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #e6a23c">
              <el-icon :size="30"><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.by_level?.一线 || 0 }}</div>
              <div class="stat-label">一线明星</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #f56c6c">
              <el-icon :size="30"><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ lastCrawlTime }}</div>
              <div class="stat-label">最后采集</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="8">
        <el-card class="coverage-card weibo">
          <div class="coverage-content">
            <div class="coverage-header">
              <span class="platform-name">微博</span>
              <el-tag type="success" size="small">{{ coverage.weibo }}%</el-tag>
            </div>
            <el-progress :percentage="coverage.weibo" :stroke-width="12" :show-text="false" />
            <div class="coverage-detail">
              <span>{{ stats.total_weibo || 0 }} / {{ stats.total_stars || 0 }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="coverage-card douyin">
          <div class="coverage-content">
            <div class="coverage-header">
              <span class="platform-name">抖音</span>
              <el-tag :type="coverage.douyin > 80 ? 'success' : 'warning'" size="small">{{ coverage.douyin }}%</el-tag>
            </div>
            <el-progress :percentage="coverage.douyin" :stroke-width="12" :show-text="false" color="#e6a23c" />
            <div class="coverage-detail">
              <span>{{ stats.total_douyin || 0 }} / {{ stats.total_stars || 0 }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="coverage-card xiaohongshu">
          <div class="coverage-content">
            <div class="coverage-header">
              <span class="platform-name">小红书</span>
              <el-tag :type="coverage.xiaohongshu > 80 ? 'success' : 'danger'" size="small">{{ coverage.xiaohongshu }}%</el-tag>
            </div>
            <el-progress :percentage="coverage.xiaohongshu" :stroke-width="12" :show-text="false" color="#f56c6c" />
            <div class="coverage-detail">
              <span>{{ stats.total_xiaohongshu || 0 }} / {{ stats.total_stars || 0 }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>明星等级分布</span>
            </div>
          </template>
          <div ref="levelChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>艺人类型分布</span>
            </div>
          </template>
          <div ref="categoryChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近更新明星</span>
              <el-button type="primary" size="small" @click="$router.push('/stars')">查看全部</el-button>
            </div>
          </template>
          <el-table :data="recentStars" style="width: 100%">
            <el-table-column prop="name" label="姓名" width="120" />
            <el-table-column prop="category" label="类型" width="100" />
            <el-table-column prop="level" label="等级" width="100">
              <template #default="{ row }">
                <el-tag :type="getLevelType(row.level)">{{ row.level }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="更新时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.updated_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" link @click="$router.push(`/stars/${row.id}`)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { User, Star, TrendCharts, Clock } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { starApi } from '../api'
import { formatTime, getLevelType } from '../utils'
import dayjs from 'dayjs'

const stats = ref({})
const recentStars = ref([])
const levelChartRef = ref(null)
const categoryChartRef = ref(null)

let levelChartInstance = null
let categoryChartInstance = null

const lastCrawlTime = computed(() => {
  if (stats.value.last_crawl_time) {
    return dayjs(stats.value.last_crawl_time).format('MM-DD HH:mm')
  }
  return '未采集'
})

const coverage = computed(() => {
  const total = stats.value.total_stars || 1
  return {
    weibo: Math.round((stats.value.total_weibo || 0) / total * 100),
    douyin: Math.round((stats.value.total_douyin || 0) / total * 100),
    xiaohongshu: Math.round((stats.value.total_xiaohongshu || 0) / total * 100)
  }
})

const loadStats = async () => {
  try {
    const res = await starApi.getStats()
    stats.value = res.data
    updateCharts()
  } catch (e) {
    console.error(e)
  }
}

const loadRecentStars = async () => {
  try {
    const res = await starApi.getList({ page: 1, page_size: 5, sort_by: 'updated_at', order: 'desc' })
    recentStars.value = res.data.items
  } catch (e) {
    console.error(e)
  }
}

const updateCharts = () => {
  if (levelChartRef.value) {
    if (levelChartInstance) {
      levelChartInstance.dispose()
    }
    levelChartInstance = echarts.init(levelChartRef.value)
    const levelData = [
      { name: '顶流', value: stats.value.by_level?.顶流 || 0 },
      { name: '一线', value: stats.value.by_level?.一线 || 0 },
      { name: '二线', value: stats.value.by_level?.二线 || 0 },
      { name: '三线', value: stats.value.by_level?.三线 || 0 }
    ]
    levelChartInstance.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: '0%' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: levelData,
        emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
      }]
    })
  }

  if (categoryChartRef.value) {
    if (categoryChartInstance) {
      categoryChartInstance.dispose()
    }
    categoryChartInstance = echarts.init(categoryChartRef.value)
    const categoryData = Object.entries(stats.value.by_category || {}).map(([name, value]) => ({ name, value }))
    categoryChartInstance.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: '0%' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: categoryData,
        emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
      }]
    })
  }
}

onMounted(() => {
  loadStats()
  loadRecentStars()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (levelChartInstance) {
    levelChartInstance.dispose()
    levelChartInstance = null
  }
  if (categoryChartInstance) {
    categoryChartInstance.dispose()
    categoryChartInstance = null
  }
})

const handleResize = () => {
  levelChartInstance?.resize()
  categoryChartInstance?.resize()
}
</script>

<style scoped>
.dashboard {
  width: 100%;
}

.stat-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 5px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.coverage-card {
  transition: transform 0.2s;
}

.coverage-card:hover {
  transform: translateY(-3px);
}

.coverage-content {
  padding: 10px 0;
}

.coverage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.platform-name {
  font-size: 18px;
  font-weight: bold;
}

.coverage-detail {
  text-align: right;
  margin-top: 10px;
  color: #666;
  font-size: 14px;
}

.coverage-card.weibo .platform-name {
  color: #409eff;
}

.coverage-card.douyin .platform-name {
  color: #e6a23c;
}

.coverage-card.xiaohongshu .platform-name {
  color: #f56c6c;
}
</style>
