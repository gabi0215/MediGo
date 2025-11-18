import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import {
  Box,
  Paper,
  Typography,
  Button,
  Container,
  Alert,
} from '@mui/material'
import LocalHospitalIcon from '@mui/icons-material/LocalHospital'
import { useAuthStore } from '../stores/authStore'

// 카카오 SDK 타입 선언
declare global {
  interface Window {
    Kakao: any
  }
}

export default function LoginPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/')
    }

    // 카카오 SDK 로드
    const script = document.createElement('script')
    script.src = 'https://developers.kakao.com/sdk/js/kakao.js'
    script.async = true
    document.body.appendChild(script)

    script.onload = () => {
      if (window.Kakao && !window.Kakao.isInitialized()) {
        // TODO: 실제 카카오 앱 키로 교체
        window.Kakao.init('YOUR_KAKAO_APP_KEY')
      }
    }

    return () => {
      document.body.removeChild(script)
    }
  }, [isAuthenticated, navigate])

  const handleKakaoLogin = () => {
    if (!window.Kakao) {
      alert('카카오 SDK가 로드되지 않았습니다')
      return
    }

    window.Kakao.Auth.login({
      success: (authObj: any) => {
        console.log('카카오 로그인 성공', authObj)
        // TODO: 백엔드 API 호출하여 JWT 토큰 받기
        // const response = await api.post('/auth/kakao', {
        //   access_token: authObj.access_token
        // })
        // setAuth(response.data.user, response.data.access_token, response.data.refresh_token)
        alert('카카오 로그인 기능은 개발 중입니다.\n데모 로그인을 이용해주세요.')
      },
      fail: (err: any) => {
        console.error('카카오 로그인 실패', err)
        alert('로그인에 실패했습니다')
      },
    })
  }

  const handleDemoLogin = () => {
    // 데모용 로그인
    const demoUser = {
      id: 1,
      email: 'demo@medigo.com',
      full_name: '김데모',
      kakao_profile_image: null,
    }
    const demoAccessToken = 'demo_access_token'
    const demoRefreshToken = 'demo_refresh_token'

    useAuthStore.getState().setAuth(demoUser, demoAccessToken, demoRefreshToken)
    navigate('/')
  }

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Paper elevation={3} sx={{ p: 4, width: '100%', borderRadius: 3 }}>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <LocalHospitalIcon
              color="primary"
              sx={{ fontSize: 64, mb: 2 }}
            />
            <Typography variant="h4" gutterBottom fontWeight={700}>
              메디-고
            </Typography>
            <Typography variant="body1" color="text.secondary">
              AI 기반 약 배달 및 복약 지도 서비스
            </Typography>
          </Box>

          {searchParams.get('message') && (
            <Alert severity="info" sx={{ mb: 3 }}>
              {searchParams.get('message')}
            </Alert>
          )}

          <Button
            fullWidth
            variant="contained"
            size="large"
            onClick={handleKakaoLogin}
            sx={{
              mb: 2,
              bgcolor: '#FEE500',
              color: '#000000',
              '&:hover': {
                bgcolor: '#FDD835',
              },
            }}
          >
            카카오로 로그인
          </Button>

          <Button
            fullWidth
            variant="outlined"
            size="large"
            onClick={handleDemoLogin}
          >
            데모 로그인 (개발용)
          </Button>

          <Typography
            variant="caption"
            display="block"
            textAlign="center"
            color="text.secondary"
            sx={{ mt: 3 }}
          >
            로그인하면 서비스 이용약관 및 개인정보처리방침에 동의하게 됩니다.
          </Typography>
        </Paper>
      </Box>
    </Container>
  )
}

