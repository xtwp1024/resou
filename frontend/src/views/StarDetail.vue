<template>
  <div class="star-detail">
    <el-page-header @back="$router.back()" title="返回">
      <template #content>
        <span class="star-title">{{ star.name }}</span>
        <el-tag :type="getLevelType(star.level)" style="margin-left: 10px">{{ star.level }}</el-tag>
      </template>
    </el-page-header>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>微博数据</span>
              <el-button type="primary" size="small" @click="crawlWeibo">采集</el-button>
            </div>
          </template>
          <div v-if="star.weibo_data" class="platform-data">
            <div class="data-item">
              <span class="label">昵称</span>
              <span class="value">{{ star.weibo_data.weibo_name || '-' }}</span>
            </div>
            <div class="data-item">
              <span class="label">粉丝数</span>
              <span class="value highlight">{{ formatNumber(star.weibo_data.fans_count) }}</span>
            </div>
            <div class="data-item">
              <span class="label">关注数</span>
              <span class="value">{{ star.weibo_data.following_count || '-' }}</span>
            </div>
            <div class="data-item">
              <span class="label">微博数</span>
              <span class="value">{{ star.weibo_data.posts_count || '-' }}</span>
            </div>
            <div class="data-item">
              <span class="label">认证</span>
              <el-tag :type="star.weibo_data.verified ? 'success' : 'info'" size="small">
                {{ star.weibo_data.verified ? '已认证' : '未认证' }}
              </el-tag>
            </div>
            <div class="data-item">
              <span class="label">采集时间</span>
              <span class="value">{{ formatTime(star.weibo_data.collect_date) }}</span>
            </div>
          </div>
          <el-empty v-else description="暂无数据" />
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>抖音数据</span>
              <el-button type="primary" size="small" @click="crawlDouyin">采集</el-button>
            </div>
          </template>
          <div v-if="star.douyin_data" class="platform-data">
            <div class="data-item">
              <span class="label">昵称</span>
              <span class="value">{{ star.douyin_data.douyin_name || '-' }}</span>
            </div>
            <div class="data-item">
              <span class="label">粉丝数</span>
              <span class="value highlight">{{ formatNumber(star.douyin_data.fans_count) }}</span>
            </div>
            <div class="data-item">
              <span class="label">获赞数</span>
              <span class="value">{{ formatNumber(star.douyin_data.likes_count) }}</span>
            </div>
            <div class="data-item">
              <span class="label">视频数</span>
              <span class="value">{{ star.douyin_data.video_count || '-' }}</span>
            </div>
            <div class="data-item">
              <span class="label">认证</span>
              <el-tag :type="star.douyin_data.verified ? 'success' : 'info'" size="small">
                {{ star.douyin_data.verified ? '已认证' : '未认证' }}
              </el-tag>
            </div>
            <div class="data-item">
              <span class="label">采集时间</span>
              <span class="value">{{ formatTime(star.douyin_data.collect_date) }}</span>
            </div>
          </div>
          <el-empty v-else description="暂无数据" />
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>小红书数据</span>
              <el-button type="primary" size="small" @click="crawlXiaohongshu">采集</el-button>
            </div>
          </template>
          <div v-if="star.xiaohongshu_data" class="platform-data">
            <div class="data-item">
              <span class="label">昵称</span>
              <span class="value">{{ star.xiaohongshu_data.xhs_name || '-' }}</span>
            </div>
            <div class="data-item">
              <span class="label">粉丝数</span>
              <span class="value highlight">{{ formatNumber(star.xiaohongshu_data.fans_count) }}</span>
            </div>
            <div class="data-item">
              <span class="label">获赞收藏</span>
              <span class="value">{{ formatNumber(star.xiaohongshu_data.likes_collects_count) }}</span>
            </div>
            <div class="data-item">
              <span class="label">笔记数</span>
              <span class="value">{{ star.xiaohongshu_data.notes_count || '-' }}</span>
            </div>
            <div class="data-item">
              <span class="label">官方账号</span>
              <el-tag :type="star.xiaohongshu_data.has_official_account ? 'success' : 'warning'" size="small">
                {{ star.xiaohongshu_data.has_official_account ? '有' : '无' }}
              </el-tag>
            </div>
            <div class="data-item">
              <span class="label">采集时间</span>
              <span class="value">{{ formatTime(star.xiaohongshu_data.collect_date) }}</span>
            </div>
          </div>
          <el-empty v-else description="暂无数据" />
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>基本信息</span>
      </template>
      <el-descriptions :column="4" border>
        <el-descriptions-item label="姓名">{{ star.name }}</el-descriptions-item>
        <el-descriptions-item label="英文名">{{ star.english_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ star.gender || '-' }}</el-descriptions-item>
        <el-descriptions-item label="类型">{{ star.category || '-' }}</el-descriptions-item>
        <el-descriptions-item label="等级">{{ star.level || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经纪公司">{{ star.agency || '-' }}</el-descriptions-item>
        <el-descriptions-item label="生日">{{ star.birthday || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatTime(star.created_at) }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { starApi, crawlApi } from '../api'
import { formatTime, formatNumber, getLevelType } from '../utils'

const route = useRoute()
const star = ref({})

const loadStar = async () => {
  try {
    const res = await starApi.getDetail(route.params.id)
    star.value = res.data
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

const crawlWeibo = async () => {
  try {
    ElMessage.info('开始采集微博数据...')
    await crawlApi.crawlWeibo(route.params.id)
    ElMessage.success('采集完成')
    loadStar()
  } catch (e) {
    ElMessage.error('采集失败')
  }
}

const crawlDouyin = async () => {
  try {
    ElMessage.info('开始采集抖音数据...')
    await crawlApi.crawlDouyin(route.params.id)
    ElMessage.success('采集完成')
    loadStar()
  } catch (e) {
    ElMessage.error('采集失败')
  }
}

const crawlXiaohongshu = async () => {
  try {
    ElMessage.info('开始采集小红书数据...')
    await crawlApi.crawlXiaohongshu(route.params.id)
    ElMessage.success('采集完成')
    loadStar()
  } catch (e) {
    ElMessage.error('采集失败')
  }
}

onMounted(() => loadStar())
</script>

<style scoped>
.star-title {
  font-size: 18px;
  font-weight: bold;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.platform-data {
  padding: 10px 0;
}

.data-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.data-item:last-child {
  border-bottom: none;
}

.data-item .label {
  color: #666;
}

.data-item .value {
  font-weight: 500;
}

.data-item .value.highlight {
  color: #409eff;
  font-size: 18px;
}
</style>
