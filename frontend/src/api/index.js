import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    let message = '请求失败'
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = error.response.data?.message || '请求参数错误'
          break
        case 401:
          message = '未授权，请重新登录'
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求地址不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = error.response.data?.message || `请求错误 (${error.response.status})`
      }
    } else if (error.request) {
      message = '网络错误，请检查网络连接'
    } else {
      message = error.message || '请求配置错误'
    }
    
    if (!error.config?.skipErrorMessage) {
      ElMessage.error(message)
    }
    
    return Promise.reject(error)
  }
)

export const starApi = {
  getList(params) {
    return api.get('/stars', { params })
  },
  getDetail(id) {
    return api.get(`/stars/${id}`)
  },
  create(data) {
    return api.post('/stars', data)
  },
  update(id, data) {
    return api.put(`/stars/${id}`, data)
  },
  delete(id) {
    return api.delete(`/stars/${id}`)
  },
  getStats() {
    return api.get('/stars/stats')
  }
}

export const crawlApi = {
  crawlWeibo(starId) {
    return api.post(`/crawl/weibo/${starId}`)
  },
  crawlDouyin(starId) {
    return api.post(`/crawl/douyin/${starId}`)
  },
  crawlXiaohongshu(starId) {
    return api.post(`/crawl/xiaohongshu/${starId}`)
  },
  crawlAll() {
    return api.post('/crawl/all')
  },
  getStatus() {
    return api.get('/crawl/status')
  }
}

export default api
