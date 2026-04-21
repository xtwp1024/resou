<template>
  <div class="crawl-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据采集</span>
          <el-button type="primary" @click="crawlAll" :loading="crawling">
            <el-icon><Refresh /></el-icon>
            一键采集全部
          </el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-card shadow="hover" class="status-card">
            <div class="status-content">
              <el-icon :size="40" color="#409eff"><Connection /></el-icon>
              <div class="status-info">
                <div class="status-label">采集状态</div>
                <div class="status-value">
                  <el-tag :type="status.is_running ? 'warning' : 'success'">
                    {{ status.is_running ? '采集中' : '空闲' }}
                  </el-tag>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="status-card">
            <div class="status-content">
              <el-icon :size="40" color="#67c23a"><DataLine /></el-icon>
              <div class="status-info">
                <div class="status-label">采集进度</div>
                <div class="status-value">{{ status.current }} / {{ status.total }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="status-card">
            <div class="status-content">
              <el-icon :size="40" color="#e6a23c"><Clock /></el-icon>
              <div class="status-info">
                <div class="status-label">最后采集</div>
                <div class="status-value">{{ formatTime(status.last_run, 'YYYY-MM-DD HH:mm:ss', '未采集') }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-divider />

      <div class="crawl-settings">
        <h3>采集设置</h3>
        <el-form label-width="100px">
          <el-form-item label="采集时间">
            <el-time-select
              v-model="crawlTime"
              start="00:00"
              end="23:30"
              step="00:30"
              placeholder="选择时间"
            />
            <span style="margin-left: 10px; color: #999">每日自动采集时间</span>
          </el-form-item>
          <el-form-item label="采集平台">
            <el-checkbox-group v-model="platforms">
              <el-checkbox label="weibo">微博</el-checkbox>
              <el-checkbox label="douyin">抖音</el-checkbox>
              <el-checkbox label="xiaohongshu">小红书</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </div>

      <el-divider />

      <div class="crawl-log">
        <h3>采集日志</h3>
        <el-table :data="status.errors" max-height="300">
          <el-table-column label="错误信息">
            <template #default="{ row }">
              <el-text type="danger">{{ row.message || row }}</el-text>
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-if="!status.errors?.length" description="暂无错误日志" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Refresh, Connection, DataLine, Clock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { crawlApi } from '../api'
import { formatTime } from '../utils'

const crawling = ref(false)
const status = ref({
  is_running: false,
  last_run: null,
  total: 0,
  current: 0,
  errors: []
})
const crawlTime = ref('02:00')
const platforms = ref(['weibo', 'douyin', 'xiaohongshu'])

const timer = ref(null)

const loadStatus = async () => {
  try {
    const res = await crawlApi.getStatus()
    status.value = res.data
  } catch (e) {
    console.error(e)
  }
}

const crawlAll = async () => {
  crawling.value = true
  try {
    await crawlApi.crawlAll()
    ElMessage.success('采集任务已启动')
    loadStatus()
  } catch (e) {
    ElMessage.error('启动失败')
  } finally {
    crawling.value = false
  }
}

onMounted(() => {
  loadStatus()
  timer.value = setInterval(loadStatus, 5000)
})

onUnmounted(() => {
  if (timer.value) clearInterval(timer.value)
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-card {
  cursor: pointer;
}

.status-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.status-info {
  flex: 1;
}

.status-label {
  font-size: 14px;
  color: #999;
}

.status-value {
  font-size: 20px;
  font-weight: bold;
  margin-top: 5px;
}

.crawl-settings h3,
.crawl-log h3 {
  margin-bottom: 20px;
  color: #333;
}
</style>
