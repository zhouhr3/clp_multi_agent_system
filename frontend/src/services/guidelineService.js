import axios from 'axios';

// 使用与其他服务相同的API实例
const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器，添加认证令牌
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 治疗指南服务
const guidelineService = {
  // 获取治疗指南列表
  async getGuidelines(page = 1, size = 10) {
    try {
      const response = await api.get('/guidelines', { params: { page, size } });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 获取单个治疗指南详情
  async getGuideline(conditionId) {
    try {
      const response = await api.get(`/guidelines/${conditionId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 创建新治疗指南（仅医生）
  async createGuideline(guidelineData) {
    try {
      const response = await api.post('/guidelines', guidelineData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 更新治疗指南（仅医生）
  async updateGuideline(conditionId, guidelineData) {
    try {
      const response = await api.put(`/guidelines/${conditionId}`, guidelineData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 删除治疗指南（仅管理员）
  async deleteGuideline(conditionId) {
    try {
      await api.delete(`/guidelines/${conditionId}`);
      return true;
    } catch (error) {
      throw error;
    }
  }
};

export default guidelineService;
