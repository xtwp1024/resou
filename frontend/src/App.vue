<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <div class="logo">明星数据系统</div>
      <el-menu
        :default-active="$route.path"
        router
        class="el-menu-vertical"
      >
        <el-menu-item index="/">
          <el-icon><DataLine /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/stars">
          <el-icon><User /></el-icon>
          <span>明星列表</span>
        </el-menu-item>
        <el-menu-item index="/rank">
          <el-icon><Trophy /></el-icon>
          <span>粉丝排行</span>
        </el-menu-item>
        <el-menu-item index="/crawl">
          <el-icon><Refresh /></el-icon>
          <span>数据采集</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div class="header-title">明星社交媒体数据采集系统</div>
        <div class="header-actions">
          <el-tag type="success">在线</el-tag>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { DataLine, User, Refresh, Trophy } from '@element-plus/icons-vue'
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-aside {
  background: #304156;
  color: #fff;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
  border-bottom: 1px solid #3a3a3a;
}

.el-menu-vertical {
  border-right: none;
  background: #304156;
}

.el-menu-item {
  color: #bfcbd9;
}

.el-menu-item:hover,
.el-menu-item.is-active {
  background: #263445 !important;
  color: #409eff;
}

.el-header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.header-title {
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-main {
  background: #f0f2f5;
  padding: 20px;
}
</style>
