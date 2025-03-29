import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Paper, 
  Card, 
  CardContent, 
  CardHeader,
  List,
  ListItem,
  ListItemText,
  Divider,
  Button,
  CircularProgress,
  Alert
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import patientService from '../services/patientService';
import analysisService from '../services/analysisService';

const Dashboard = () => {
  const { currentUser } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [patients, setPatients] = useState([]);
  const [recentAnalyses, setRecentAnalyses] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      setError('');
      try {
        // 获取患者列表
        const patientsData = await patientService.getPatients(1, 5);
        setPatients(patientsData.items);
        
        // 获取最近的分析结果
        const analysesData = await analysisService.getAnalyses(1, 5);
        setRecentAnalyses(analysesData.items);
      } catch (err) {
        console.error('获取仪表盘数据失败:', err);
        setError('获取数据失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          仪表盘
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          欢迎回来，{currentUser?.full_name || '用户'}
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* 系统概述 */}
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              唇腭裂多智能体系统
            </Typography>
            <Typography variant="body1" paragraph>
              本系统是一个基于人工智能的医疗辅助决策系统，专门用于唇腭裂患者的诊断和治疗建议。系统采用多智能体架构，集成了多个专科智能体，能够根据患者症状和特征，动态招募相关专科智能体，提供综合的诊断和治疗建议。
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      综合征识别
                    </Typography>
                    <Typography variant="body2">
                      区分综合征性和非综合征性唇腭裂，为患者提供精准诊断
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      多专科协作
                    </Typography>
                    <Typography variant="body2">
                      集成唇腭裂专科、颅面外科、遗传学、外耳科和眼科等多个专科智能体
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      个性化治疗
                    </Typography>
                    <Typography variant="body2">
                      根据患者具体情况提供个性化的治疗方案和随访计划
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* 最近患者 */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ height: '100%' }}>
            <CardHeader 
              title="最近患者" 
              action={
                <Button size="small" onClick={() => window.location.href = '/patients'}>
                  查看全部
                </Button>
              }
            />
            <Divider />
            <CardContent>
              {patients.length > 0 ? (
                <List>
                  {patients.map((patient) => (
                    <React.Fragment key={patient.id}>
                      <ListItem button onClick={() => window.location.href = `/patients/${patient.id}`}>
                        <ListItemText 
                          primary={patient.name} 
                          secondary={`${patient.age} | ${patient.gender} | 症状: ${patient.symptoms.join(', ')}`} 
                        />
                      </ListItem>
                      <Divider component="li" />
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary" align="center">
                  暂无患者记录
                </Typography>
              )}
            </CardContent>
          </Paper>
        </Grid>

        {/* 最近分析 */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ height: '100%' }}>
            <CardHeader 
              title="最近分析结果" 
              action={
                <Button size="small" onClick={() => window.location.href = '/analysis'}>
                  新建分析
                </Button>
              }
            />
            <Divider />
            <CardContent>
              {recentAnalyses.length > 0 ? (
                <List>
                  {recentAnalyses.map((analysis) => (
                    <React.Fragment key={analysis.id}>
                      <ListItem>
                        <ListItemText 
                          primary={`患者ID: ${analysis.patient_id} | ${analysis.syndrome_type === 'syndromic' ? '综合征性' : '非综合征性'}`} 
                          secondary={`类型: ${analysis.cleft_type} | 严重程度: ${analysis.severity} | 分析时间: ${new Date(analysis.analyzed_at).toLocaleString()}`} 
                        />
                      </ListItem>
                      <Divider component="li" />
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary" align="center">
                  暂无分析记录
                </Typography>
              )}
            </CardContent>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
