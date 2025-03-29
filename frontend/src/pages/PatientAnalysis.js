import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Paper, 
  Button, 
  TextField, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Chip,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  CardHeader,
  Divider,
  List,
  ListItem,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { useFormik } from 'formik';
import * as yup from 'yup';
import analysisService from '../services/analysisService';
import patientService from '../services/patientService';

// 验证模式
const validationSchema = yup.object({
  symptoms: yup
    .string()
    .required('症状是必填项'),
  age: yup
    .string()
    .required('年龄是必填项'),
  gender: yup
    .string()
    .required('性别是必填项'),
});

const PatientAnalysis = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [patients, setPatients] = useState([]);
  const [loadingPatients, setLoadingPatients] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [openPatientDialog, setOpenPatientDialog] = useState(false);

  // 获取患者列表
  useEffect(() => {
    const fetchPatients = async () => {
      setLoadingPatients(true);
      try {
        const response = await patientService.getPatients(1, 100);
        setPatients(response.items);
      } catch (err) {
        console.error('获取患者列表失败:', err);
      } finally {
        setLoadingPatients(false);
      }
    };

    fetchPatients();
  }, []);

  // 处理表单提交
  const formik = useFormik({
    initialValues: {
      symptoms: '',
      age: '',
      gender: '',
      medical_history: '',
      family_history: '',
    },
    validationSchema: validationSchema,
    onSubmit: async (values) => {
      setLoading(true);
      setError('');
      setAnalysisResult(null);
      
      try {
        // 将症状字符串转换为数组
        const symptomsArray = values.symptoms.split(',').map(s => s.trim());
        
        const analysisData = {
          symptoms: symptomsArray,
          age: values.age,
          gender: values.gender,
          medical_history: values.medical_history || null,
          family_history: values.family_history || null,
        };
        
        const result = await analysisService.analyzePatientData(analysisData);
        setAnalysisResult(result);
      } catch (err) {
        console.error('分析患者数据失败:', err);
        setError('分析失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    },
  });

  // 处理选择患者
  const handleSelectPatient = (patient) => {
    setSelectedPatient(patient);
    formik.setValues({
      symptoms: patient.symptoms.join(', '),
      age: patient.age,
      gender: patient.gender,
      medical_history: patient.medical_history || '',
      family_history: patient.family_history || '',
    });
    setOpenPatientDialog(false);
  };

  // 处理分析特定患者
  const handleAnalyzePatient = async (patientId) => {
    setLoading(true);
    setError('');
    setAnalysisResult(null);
    
    try {
      const result = await analysisService.analyzePatient(patientId);
      setAnalysisResult(result);
    } catch (err) {
      console.error('分析患者失败:', err);
      setError('分析失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          患者分析
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          使用多智能体系统分析患者数据，提供诊断和治疗建议
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* 分析表单 */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="h6" gutterBottom>
                输入患者信息
              </Typography>
              <Button 
                variant="outlined" 
                size="small"
                onClick={() => setOpenPatientDialog(true)}
                disabled={loadingPatients || patients.length === 0}
              >
                选择已有患者
              </Button>
            </Box>
            
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            
            <Box component="form" onSubmit={formik.handleSubmit} noValidate>
              <TextField
                margin="normal"
                required
                fullWidth
                id="symptoms"
                name="symptoms"
                label="症状"
                placeholder="请输入症状，多个症状用逗号分隔"
                value={formik.values.symptoms}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                error={formik.touched.symptoms && Boolean(formik.errors.symptoms)}
                helperText={formik.touched.symptoms && formik.errors.symptoms}
              />
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="age"
                    name="age"
                    label="年龄"
                    placeholder="例如：5岁"
                    value={formik.values.age}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={formik.touched.age && Boolean(formik.errors.age)}
                    helperText={formik.touched.age && formik.errors.age}
                  />
                </Grid>
                <Grid item xs={6}>
                  <FormControl 
                    fullWidth 
                    margin="normal"
                    error={formik.touched.gender && Boolean(formik.errors.gender)}
                  >
                    <InputLabel id="gender-label">性别</InputLabel>
                    <Select
                      labelId="gender-label"
                      id="gender"
                      name="gender"
                      value={formik.values.gender}
                      label="性别"
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                    >
                      <MenuItem value="男">男</MenuItem>
                      <MenuItem value="女">女</MenuItem>
                    </Select>
                    {formik.touched.gender && formik.errors.gender && (
                      <Typography variant="caption" color="error">
                        {formik.errors.gender}
                      </Typography>
                    )}
                  </FormControl>
                </Grid>
              </Grid>
              
              <TextField
                margin="normal"
                fullWidth
                id="medical_history"
                name="medical_history"
                label="病史"
                multiline
                rows={2}
                placeholder="请输入患者病史（可选）"
                value={formik.values.medical_history}
                onChange={formik.handleChange}
              />
              
              <TextField
                margin="normal"
                fullWidth
                id="family_history"
                name="family_history"
                label="家族史"
                multiline
                rows={2}
                placeholder="请输入患者家族史（可选）"
                value={formik.values.family_history}
                onChange={formik.handleChange}
              />
              
              <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
                <Button
                  variant="outlined"
                  onClick={() => formik.resetForm()}
                  disabled={loading}
                >
                  重置
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : '分析患者'}
                </Button>
              </Box>
              
              {selectedPatient && (
                <Box sx={{ mt: 2 }}>
                  <Chip 
                    label={`已选择患者: ${selectedPatient.name}`} 
                    color="primary" 
                    onDelete={() => setSelectedPatient(null)}
                    sx={{ mr: 1 }}
                  />
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => handleAnalyzePatient(selectedPatient.id)}
                    disabled={loading}
                  >
                    直接分析此患者
                  </Button>
                </Box>
              )}
            </Box>
          </Paper>
        </Grid>
        
        {/* 分析结果 */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              分析结果
            </Typography>
            
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
                <CircularProgress />
              </Box>
            ) : analysisResult ? (
              <Box>
                <Card variant="outlined" sx={{ mb: 2 }}>
                  <CardHeader 
                    title="综合征判断" 
                    subheader={analysisResult.syndrome_type === 'syndromic' ? '综合征性唇腭裂' : '非综合征性唇腭裂'} 
                  />
                  <Divider />
                  <CardContent>
                    {analysisResult.syndrome_type === 'syndromic' && (
                      <Typography variant="body1" gutterBottom>
                        综合征名称: {analysisResult.syndrome_name || '未指定'}
                      </Typography>
                    )}
                    <Typography variant="body1" gutterBottom>
                      唇腭裂类型: {analysisResult.cleft_type}
                    </Typography>
                    <Typography variant="body1">
                      严重程度: {analysisResult.severity}
                    </Typography>
                  </CardContent>
                </Card>
                
                <Card variant="outlined" sx={{ mb: 2 }}>
                  <CardHeader title="治疗建议" />
                  <Divider />
                  <CardContent>
                    <List dense>
                      {Object.entries(analysisResult.treatment_recommendations).map(([key, value]) => (
                        <ListItem key={key}>
                          <ListItemText 
                            primary={key} 
                            secondary={value} 
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
                
                {analysisResult.specialist_recommendations && (
                  <Card variant="outlined" sx={{ mb: 2 }}>
                    <CardHeader title="专科会诊建议" />
                    <Divider />
                    <CardContent>
                      <List dense>
                        {Object.entries(analysisResult.specialist_recommendations).map(([key, value]) => (
                          <ListItem key={key}>
                            <ListItemText 
                              primary={key} 
                              secondary={value} 
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                )}
                
                {analysisResult.follow_up_plan && (
                  <Card variant="outlined">
                    <CardHeader title="随访计划" />
                    <Divider />
                    <CardContent>
                      <List dense>
                        {Object.entries(analysisResult.follow_up_plan).map(([key, value]) => (
                          <ListItem key={key}>
                            <ListItemText 
                              primary={key} 
                              secondary={value} 
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                )}
              </Box>
            ) : (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
                <Typography variant="body1" color="text.secondary">
                  请输入患者信息并点击"分析患者"按钮
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
      
      {/* 患者选择对话框 */}
      <Dialog open={openPatientDialog} onClose={() => setOpenPatientDialog(false)}>
        <DialogTitle>选择患者</DialogTitle>
        <DialogContent>
          {loadingPatients ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress />
            </Box>
          ) : patients.length > 0 ? (
            <List sx={{ minWidth: 300 }}>
              {patients.map((patient) => (
                <ListItem 
                  button 
                  key={patient.id}
                  onClick={() => handleSelectPatient(patient)}
                >
                  <ListItemText 
                    primary={patient.name} 
                    secondary={`${patient.age} | ${patient.gender} | 症状: ${patient.symptoms.join(', ')}`} 
                  />
                </ListItem>
              ))}
            </List>
          ) : (
            <Typography variant="body1" color="text.secondary">
              暂无患者记录
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenPatientDialog(false)}>取消</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default PatientAnalysis;
