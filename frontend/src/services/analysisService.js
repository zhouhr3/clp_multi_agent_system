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

// 分析服务
const analysisService = {
  // 获取分析结果列表
  async getAnalyses(page = 1, size = 10, patientId = null) {
    try {
      const params = { page, size };
      if (patientId) {
        params.patient_id = patientId;
      }
      const response = await api.get('/analyses', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 获取单个分析结果详情
  async getAnalysis(id) {
    try {
      const response = await api.get(`/analyses/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 分析患者数据（不保存）
  async analyzePatientData(analysisData) {
    try {
      const response = await api.post('/analyses/analyze', analysisData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 分析特定患者并保存结果
  async analyzePatient(patientId) {
    try {
      const response = await api.post(`/analyses/patient/${patientId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 创建新分析结果
  async createAnalysis(analysisData) {
    try {
      const response = await api.post('/analyses', analysisData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 更新分析结果
  async updateAnalysis(id, analysisData) {
    try {
      const response = await api.put(`/analyses/${id}`, analysisData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 删除分析结果
  async deleteAnalysis(id) {
    try {
      await api.delete(`/analyses/${id}`);
      return true;
    } catch (error) {
      throw error;
    }
  }
};

export default analysisService;
