import { useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Paper,
} from '@mui/material'
import LocalHospitalIcon from '@mui/icons-material/LocalHospital'
import CameraAltIcon from '@mui/icons-material/CameraAlt'
import LocalShippingIcon from '@mui/icons-material/LocalShipping'
import DescriptionIcon from '@mui/icons-material/Description'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <Box>
      {/* Hero Section */}
      <Paper
        elevation={0}
        sx={{
          p: 4,
          mb: 4,
          bgcolor: 'primary.main',
          color: 'white',
          borderRadius: 3,
          textAlign: 'center',
        }}
      >
        <LocalHospitalIcon sx={{ fontSize: 60, mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          메디-고
        </Typography>
        <Typography variant="h6" sx={{ mb: 3, opacity: 0.9 }}>
          AI 기반 약 배달 및 복약 지도 서비스
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/order')}
          sx={{
            bgcolor: 'white',
            color: 'primary.main',
            '&:hover': {
              bgcolor: 'grey.100',
            },
          }}
        >
          처방전 접수하기
        </Button>
      </Paper>

      {/* How it works */}
      <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        이용 방법
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center', p: 3 }}>
              <CameraAltIcon color="primary" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                1. 처방전 촬영
              </Typography>
              <Typography variant="body2" color="text.secondary">
                병원에서 받은 처방전을 촬영하여 업로드합니다
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center', p: 3 }}>
              <LocalShippingIcon color="primary" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                2. 약 배달
              </Typography>
              <Typography variant="body2" color="text.secondary">
                약국에서 조제 후 집으로 안전하게 배달됩니다
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center', p: 3 }}>
              <DescriptionIcon color="primary" sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                3. 복약 지도
              </Typography>
              <Typography variant="body2" color="text.secondary">
                복약 방법을 명확하게 안내받습니다
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* CTA Section */}
      <Box sx={{ textAlign: 'center', mt: 6 }}>
        <Button
          variant="outlined"
          size="large"
          onClick={() => navigate('/orders')}
          sx={{ mr: 2 }}
        >
          주문 내역 보기
        </Button>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/order')}
        >
          새 주문하기
        </Button>
      </Box>
    </Box>
  )
}

