import axios from 'axios';

// 创建axios实例
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

// 响应拦截器，处理错误
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 处理401错误（未授权）
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 认证服务
const authService = {
  // 登录
  async login(email, password) {
    try {
      const response = await api.post('/users/login', { email, password });
      const { access_token, token_type } = response.data;
      localStorage.setItem('token', access_token);
      
      // 获取用户信息
      const userResponse = await this.getCurrentUser();
      return { token: access_token, user: userResponse };
    } catch (error) {
      throw error;
    }
  },

  // 注册
  async register(userData) {
    try {
      const response = await api.post('/users/register', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 获取当前用户信息
  async getCurrentUser() {
    try {
      const response = await api.get('/users/me');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 更新用户信息
  async updateUser(userData) {
    try {
      const response = await api.put('/users/me', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 登出
  logout() {
    localStorage.removeItem('token');
  },

  // 检查是否已认证
  isAuthenticated() {
    return !!localStorage.getItem('token');
  }
};

export default authService;
