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

// 医学文献服务
const literatureService = {
  // 获取医学文献列表
  async getLiteratures(page = 1, size = 10) {
    try {
      const response = await api.get('/literature', { params: { page, size } });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 获取单个医学文献详情
  async getLiterature(pubmedId) {
    try {
      const response = await api.get(`/literature/${pubmedId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 搜索医学文献
  async searchLiterature(query, maxResults = 10, sortBy = 'relevance', dateRange = null) {
    try {
      const params = {
        query,
        max_results: maxResults,
        sort_by: sortBy
      };
      
      if (dateRange) {
        params.date_range = dateRange;
      }
      
      const response = await api.get('/literature/search', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 创建新医学文献记录（仅医生）
  async createLiterature(literatureData) {
    try {
      const response = await api.post('/literature', literatureData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 更新医学文献记录（仅医生）
  async updateLiterature(pubmedId, literatureData) {
    try {
      const response = await api.put(`/literature/${pubmedId}`, literatureData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 删除医学文献记录（仅医生）
  async deleteLiterature(pubmedId) {
    try {
      await api.delete(`/literature/${pubmedId}`);
      return true;
    } catch (error) {
      throw error;
    }
  }
};

export default literatureService;
