import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  TextField, 
  Button, 
  Paper, 
  Box, 
  Grid, 
  Avatar, 
  Link,
  Alert,
  CircularProgress
} from '@mui/material';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useFormik } from 'formik';
import * as yup from 'yup';

// 验证模式
const validationSchema = yup.object({
  full_name: yup
    .string()
    .required('姓名是必填项'),
  email: yup
    .string()
    .email('请输入有效的电子邮箱')
    .required('电子邮箱是必填项'),
  password: yup
    .string()
    .min(6, '密码至少需要6个字符')
    .required('密码是必填项'),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref('password'), null], '密码不匹配')
    .required('确认密码是必填项'),
});

const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const formik = useFormik({
    initialValues: {
      full_name: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
    validationSchema: validationSchema,
    onSubmit: async (values) => {
      setLoading(true);
      setError('');
      try {
        const userData = {
          full_name: values.full_name,
          email: values.email,
          password: values.password,
        };
        
        const result = await register(userData);
        if (result.success) {
          navigate('/login');
        } else {
          setError(result.message || '注册失败，请稍后重试');
        }
      } catch (err) {
        setError('注册过程中发生错误，请稍后重试');
        console.error('注册错误:', err);
      } finally {
        setLoading(false);
      }
    },
  });

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
          <PersonAddIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          注册
        </Typography>
        <Paper elevation={3} sx={{ p: 4, mt: 3, width: '100%' }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <Box component="form" onSubmit={formik.handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="full_name"
              label="姓名"
              name="full_name"
              autoComplete="name"
              autoFocus
              value={formik.values.full_name}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.full_name && Boolean(formik.errors.full_name)}
              helperText={formik.touched.full_name && formik.errors.full_name}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="电子邮箱"
              name="email"
              autoComplete="email"
              value={formik.values.email}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.email && Boolean(formik.errors.email)}
              helperText={formik.touched.email && formik.errors.email}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="密码"
              type="password"
              id="password"
              autoComplete="new-password"
              value={formik.values.password}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.password && Boolean(formik.errors.password)}
              helperText={formik.touched.password && formik.errors.password}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="confirmPassword"
              label="确认密码"
              type="password"
              id="confirmPassword"
              autoComplete="new-password"
              value={formik.values.confirmPassword}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.confirmPassword && Boolean(formik.errors.confirmPassword)}
              helperText={formik.touched.confirmPassword && formik.errors.confirmPassword}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : '注册'}
            </Button>
            <Grid container>
              <Grid item>
                <Link component={RouterLink} to="/login" variant="body2">
                  {"已有账号？登录"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Paper>
      </Box>
      <Box mt={8} textAlign="center">
        <Typography variant="body2" color="text.secondary">
          唇腭裂多智能体系统 - 基于人工智能的医疗辅助决策系统
        </Typography>
      </Box>
    </Container>
  );
};

export default Register;
