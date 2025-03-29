import axios from 'axios';

// 使用与authService相同的API实例
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

// 患者服务
const patientService = {
  // 获取患者列表
  async getPatients(page = 1, size = 10) {
    try {
      const response = await api.get('/patients', { params: { page, size } });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 获取单个患者详情
  async getPatient(id) {
    try {
      const response = await api.get(`/patients/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 创建新患者
  async createPatient(patientData) {
    try {
      const response = await api.post('/patients', patientData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 更新患者信息
  async updatePatient(id, patientData) {
    try {
      const response = await api.put(`/patients/${id}`, patientData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 删除患者
  async deletePatient(id) {
    try {
      await api.delete(`/patients/${id}`);
      return true;
    } catch (error) {
      throw error;
    }
  }
};

export default patientService;
