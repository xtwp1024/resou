<template>
  <div class="stars-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>明星列表 (共 {{ total }} 人)</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>
            添加明星
          </el-button>
        </div>
      </template>

      <div class="filter-bar">
        <el-input
          v-model="keyword"
          placeholder="搜索明星姓名"
          style="width: 200px"
          clearable
          @clear="loadStars"
          @keyup.enter="loadStars"
        >
          <template #append>
            <el-button @click="loadStars">搜索</el-button>
          </template>
        </el-input>
        <el-select v-model="filterLevel" placeholder="等级筛选" clearable @change="loadStars" style="width: 120px">
          <el-option label="顶流" value="顶流" />
          <el-option label="一线" value="一线" />
          <el-option label="二线" value="二线" />
          <el-option label="三线" value="三线" />
        </el-select>
        <el-select v-model="filterCategory" placeholder="类型筛选" clearable @change="loadStars" style="width: 150px">
          <el-option label="演员" value="演员" />
          <el-option label="歌手" value="歌手" />
          <el-option label="主持人" value="主持人" />
          <el-option label="偶像" value="偶像" />
          <el-option label="导演" value="导演" />
          <el-option label="其他" value="其他" />
        </el-select>
        <el-select v-model="sortBy" placeholder="排序方式" @change="loadStars" style="width: 140px">
          <el-option label="更新时间" value="updated_at" />
          <el-option label="微博粉丝" value="weibo_fans" />
          <el-option label="抖音粉丝" value="douyin_fans" />
          <el-option label="小红书粉丝" value="xiaohongshu_fans" />
        </el-select>
      </div>

      <el-table :data="stars" v-loading="loading" style="width: 100%">
        <el-table-column prop="name" label="姓名" width="140">
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
        <el-table-column label="微博粉丝" width="120">
          <template #default="{ row }">
            <div class="fans-cell weibo">
              <span v-if="row.weibo_fans">{{ formatNumber(row.weibo_fans) }}</span>
              <span v-else class="no-data">-</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="抖音粉丝" width="120">
          <template #default="{ row }">
            <div class="fans-cell douyin">
              <span v-if="row.douyin_fans">{{ formatNumber(row.douyin_fans) }}</span>
              <span v-else class="no-data">-</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="小红书粉丝" width="120">
          <template #default="{ row }">
            <div class="fans-cell xiaohongshu">
              <span v-if="row.xiaohongshu_fans">{{ formatNumber(row.xiaohongshu_fans) }}</span>
              <span v-else class="no-data">-</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="agency" label="经纪公司" width="150" show-overflow-tooltip />
        <el-table-column label="更新时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="$router.push(`/stars/${row.id}`)">详情</el-button>
            <el-button type="warning" link @click="handleCrawl(row)">采集</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="loadStars"
          @current-change="loadStars"
        />
      </div>
    </el-card>

    <el-dialog v-model="showAddDialog" title="添加明星" width="500px">
      <el-form :model="newStar" label-width="80px">
        <el-form-item label="姓名" required>
          <el-input v-model="newStar.name" />
        </el-form-item>
        <el-form-item label="英文名">
          <el-input v-model="newStar.english_name" />
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="newStar.gender">
            <el-radio label="男">男</el-radio>
            <el-radio label="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="newStar.category" style="width: 100%">
            <el-option label="演员" value="演员" />
            <el-option label="歌手" value="歌手" />
            <el-option label="主持人" value="主持人" />
            <el-option label="偶像" value="偶像" />
          </el-select>
        </el-form-item>
        <el-form-item label="等级">
          <el-select v-model="newStar.level" style="width: 100%">
            <el-option label="顶流" value="顶流" />
            <el-option label="一线" value="一线" />
            <el-option label="二线" value="二线" />
            <el-option label="三线" value="三线" />
          </el-select>
        </el-form-item>
        <el-form-item label="经纪公司">
          <el-input v-model="newStar.agency" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { starApi, crawlApi } from '../api'
import { formatTime, formatNumber, getLevelType, getLevelClass } from '../utils'

const loading = ref(false)
const stars = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const keyword = ref('')
const filterLevel = ref('')
const filterCategory = ref('')
const sortBy = ref('updated_at')
const showAddDialog = ref(false)
const newStar = ref({
  name: '',
  english_name: '',
  gender: '女',
  category: '演员',
  level: '一线',
  agency: ''
})

const loadStars = async () => {
  loading.value = true
  try {
    const res = await starApi.getList({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value,
      level: filterLevel.value,
      category: filterCategory.value,
      sort_by: sortBy.value
    })
    stars.value = res.data.items
    total.value = res.data.total
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = async () => {
  if (!newStar.value.name) {
    ElMessage.warning('请输入明星姓名')
    return
  }
  try {
    await starApi.create(newStar.value)
    ElMessage.success('添加成功')
    showAddDialog.value = false
    newStar.value = { name: '', english_name: '', gender: '女', category: '演员', level: '一线', agency: '' }
    loadStars()
  } catch (e) {
    ElMessage.error('添加失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除 ${row.name} 吗？`, '提示', { type: 'warning' })
    await starApi.delete(row.id)
    ElMessage.success('删除成功')
    loadStars()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

const handleCrawl = async (row) => {
  try {
    ElMessage.info(`开始采集 ${row.name} 的数据...`)
    const results = await Promise.allSettled([
      crawlApi.crawlWeibo(row.id),
      crawlApi.crawlDouyin(row.id),
      crawlApi.crawlXiaohongshu(row.id)
    ])
    
    const failedCount = results.filter(r => r.status === 'rejected').length
    if (failedCount === 0) {
      ElMessage.success('采集完成')
    } else if (failedCount < 3) {
      ElMessage.warning(`部分平台采集成功，${failedCount} 个平台失败`)
    } else {
      ElMessage.error('所有平台采集失败')
    }
    loadStars()
  } catch (e) {
    ElMessage.error('采集失败')
  }
}

onMounted(() => loadStars())
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
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

.fans-cell {
  font-weight: 500;
}

.fans-cell.weibo {
  color: #409eff;
}

.fans-cell.douyin {
  color: #e6a23c;
}

.fans-cell.xiaohongshu {
  color: #f56c6c;
}

.no-data {
  color: #ccc;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
