import dayjs from 'dayjs'

export const formatNumber = (num) => {
  if (!num) return '-'
  if (num >= 100000000) return (num / 100000000).toFixed(1) + '亿'
  if (num >= 10000) return (num / 10000).toFixed(1) + '万'
  return num.toLocaleString()
}

export const formatTime = (time, format = 'YYYY-MM-DD HH:mm', defaultValue = '-') => {
  return time ? dayjs(time).format(format) : defaultValue
}

export const getLevelType = (level) => {
  const types = { '顶流': 'danger', '一线': 'warning', '二线': 'success', '三线': 'info' }
  return types[level] || ''
}

export const getLevelClass = (level) => {
  const classes = { '顶流': 'top', '一线': 'first', '二线': 'second', '三线': 'third' }
  return classes[level] || ''
}
