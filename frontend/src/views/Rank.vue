<template>
  <div class="rank-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>粉丝排行榜</span>
          <el-radio-group v-model="platform" @change="loadRank">
            <el-radio-button label="weibo">微博</el-radio-button>
            <el-radio-button label="douyin">抖音</el-radio-button>
            <el-radio-button label="xiaohongshu">小红书</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <el-table :data="rankList" v-loading="loading" style="width: 100%">
        <el-table-column label="排名" width="80">
          <template #default="{ $index }">
            <div class="rank-badge" :class="getRankClass($index)">
              {{ $index + 1 }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="姓名" width="180">
          <template #default="{ row }">
            <div class="star-name">
              <el-avatar :size="40" :src="row.avatar">
                {{ row.name.charAt(0) }}
              </el-avatar>
              <div class="name-info">
                <span class="name">{{ row.name }}</span>
                <span class="level-tag" :class="getLevelClass(row.level)">{{ row.level }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="类型" width="100" />
        <el-table-column label="粉丝数" width="150">
          <template #default="{ row }">
            <span class="fans-count">{{ formatNumber(row.fans_count) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="粉丝变化" width="120">
          <template #default="{ row }">
            <span v-if="row.fans_change > 0" class="fans-up">
              <el-icon><Top /></el-icon>
              {{ formatNumber(row.fans_change) }}
            </span>
            <span v-else-if="row.fans_change < 0" class="fans-down">
              <el-icon><Bottom /></el-icon>
              {{ formatNumber(Math.abs(row.fans_change)) }}
            </span>
            <span v-else class="fans-same">-</span>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Top, Bottom } from '@element-plus/icons-vue'
import { starApi } from '../api'
import { ElMessage } from 'element-plus'
import { formatNumber, getLevelClass } from '../utils'

const loading = ref(false)
const platform = ref('weibo')
const rankList = ref([])

const getRankClass = (index) => {
  if (index === 0) return 'gold'
  if (index === 1) return 'silver'
  if (index === 2) return 'bronze'
  return ''
}

const loadRank = async () => {
  loading.value = true
  try {
    const res = await starApi.getList({
      page: 1,
      page_size: 50,
      sort_by: `${platform.value}_fans`,
      order: 'desc'
    })
    rankList.value = res.data.items
      .filter(star => star[`${platform.value}_fans`])
      .map(star => ({
        ...star,
        fans_count: star[`${platform.value}_fans`],
        fans_change: 0
      }))
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => loadRank())
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rank-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  background: #f0f0f0;
  color: #666;
}

.rank-badge.gold {
  background: linear-gradient(135deg, #ffd700, #ffec8b);
  color: #8b6914;
}

.rank-badge.silver {
  background: linear-gradient(135deg, #c0c0c0, #e8e8e8);
  color: #666;
}

.rank-badge.bronze {
  background: linear-gradient(135deg, #cd7f32, #daa06d);
  color: #fff;
}

.star-name {
  display: flex;
  align-items: center;
  gap: 10px;
}

.name-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.name-info .name {
  font-weight: 500;
}

.level-tag {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 3px;
  width: fit-content;
}

.level-tag.top {
  background: #fef0f0;
  color: #f56c6c;
}

.level-tag.first {
  background: #fdf6ec;
  color: #e6a23c;
}

.level-tag.second {
  background: #f0f9eb;
  color: #67c23a;
}

.level-tag.third {
  background: #f4f4f5;
  color: #909399;
}

.fans-count {
  font-size: 16px;
  font-weight: bold;
  color: #409eff;
}

.fans-up {
  color: #67c23a;
  display: flex;
  align-items: center;
  gap: 2px;
}

.fans-down {
  color: #f56c6c;
  display: flex;
  align-items: center;
  gap: 2px;
}

.fans-same {
  color: #ccc;
}
</style>
