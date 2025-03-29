import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../services/authService';

// 创建认证上下文
const AuthContext = createContext(null);

// 认证提供者组件
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // 初始化时检查用户是否已登录
  useEffect(() => {
    const initAuth = async () => {
      try {
        const user = await authService.getCurrentUser();
        if (user) {
          setCurrentUser(user);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('初始化认证失败:', error);
        // 清除可能存在的无效令牌
        authService.logout();
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  // 登录方法
  const login = async (email, password) => {
    try {
      const data = await authService.login(email, password);
      setCurrentUser(data.user);
      setIsAuthenticated(true);
      return { success: true };
    } catch (error) {
      console.error('登录失败:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || '登录失败，请检查您的凭据' 
      };
    }
  };

  // 注册方法
  const register = async (userData) => {
    try {
      const data = await authService.register(userData);
      return { success: true, data };
    } catch (error) {
      console.error('注册失败:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || '注册失败，请稍后重试' 
      };
    }
  };

  // 登出方法
  const logout = () => {
    authService.logout();
    setCurrentUser(null);
    setIsAuthenticated(false);
    navigate('/login');
  };

  // 更新用户信息
  const updateUserInfo = (user) => {
    setCurrentUser(user);
  };

  // 提供的上下文值
  const value = {
    currentUser,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    updateUserInfo
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// 自定义钩子，用于访问认证上下文
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth必须在AuthProvider内部使用');
  }
  return context;
};
