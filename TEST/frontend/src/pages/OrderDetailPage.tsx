import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Button,
  Divider,
  Grid,
  Paper,
  Alert,
} from '@mui/material'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'

// 임시 데이터
const mockOrder = {
  id: 1,
  status: 'completed',
  created_at: '2024-01-15T10:30:00',
  completed_at: '2024-01-15T12:00:00',
  delivery_address: '서울시 강남구 테헤란로 123',
  delivery_address_detail: '101동 1001호',
  delivery_phone: '010-1234-5678',
  delivery_note: '문 앞에 놓아주세요',
  medicine_price: 12000,
  delivery_fee: 3000,
  total_price: 15000,
  is_paid: true,
  pharmacy_name: '행복약국',
  medication_guidance: {
    guidance_text:
      '김지수님, 처방받으신 약은 다음과 같이 복용하세요.\n\n1. A약(소염진통제): 아침, 점심, 저녁 식후 30분에 1알씩 복용\n2. B약(위장약): 아침, 저녁 식후 30분에 1알씩 복용\n\n증상이 호전되지 않거나 악화되면 즉시 병원을 방문하세요.',
    is_sent: true,
    sent_at: '2024-01-15T12:05:00',
  },
}

const statusMap: Record<string, { label: string; color: any }> = {
  submitted: { label: '접수 완료', color: 'info' },
  processing: { label: '조제 중', color: 'warning' },
  delivering: { label: '배달 중', color: 'primary' },
  completed: { label: '배달 완료', color: 'success' },
  cancelled: { label: '취소됨', color: 'error' },
}

export default function OrderDetailPage() {
  const { orderId } = useParams()
  const navigate = useNavigate()

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/orders')}
        sx={{ mb: 2 }}
      >
        목록으로
      </Button>

      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" fontWeight={600} sx={{ flexGrow: 1 }}>
          주문 #{orderId}
        </Typography>
        <Chip
          label={statusMap[mockOrder.status].label}
          color={statusMap[mockOrder.status].color}
          size="medium"
        />
      </Box>

      {mockOrder.status === 'completed' && (
        <Alert icon={<CheckCircleIcon />} severity="success" sx={{ mb: 3 }}>
          배달이 완료되었습니다!
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* 배달 정보 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                배달 정보
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="body2" color="text.secondary" gutterBottom>
                주소
              </Typography>
              <Typography gutterBottom>
                {mockOrder.delivery_address}
                <br />
                {mockOrder.delivery_address_detail}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                연락처
              </Typography>
              <Typography gutterBottom>{mockOrder.delivery_phone}</Typography>
              {mockOrder.delivery_note && (
                <>
                  <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mt: 2 }}>
                    배달 메모
                  </Typography>
                  <Typography>{mockOrder.delivery_note}</Typography>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* 결제 정보 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                결제 정보
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography>약값</Typography>
                <Typography>{mockOrder.medicine_price?.toLocaleString()}원</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography>배달비</Typography>
                <Typography>{mockOrder.delivery_fee?.toLocaleString()}원</Typography>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography variant="h6">총 금액</Typography>
                <Typography variant="h6" color="primary">
                  {mockOrder.total_price?.toLocaleString()}원
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                결제 상태: {mockOrder.is_paid ? '결제 완료' : '미결제'}
              </Typography>
              {mockOrder.pharmacy_name && (
                <Typography variant="body2" color="text.secondary">
                  조제 약국: {mockOrder.pharmacy_name}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* 복약 지도 */}
        {mockOrder.medication_guidance && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3, bgcolor: 'primary.50', border: '2px solid', borderColor: 'primary.main' }}>
              <Typography variant="h6" gutterBottom color="primary">
                💊 복약 지도
              </Typography>
              <Typography
                variant="body1"
                sx={{ whiteSpace: 'pre-line', lineHeight: 1.8 }}
              >
                {mockOrder.medication_guidance.guidance_text}
              </Typography>
            </Paper>
          </Grid>
        )}

        {/* 주문 일시 */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                주문 일시: {new Date(mockOrder.created_at).toLocaleString('ko-KR')}
              </Typography>
              {mockOrder.completed_at && (
                <Typography variant="body2" color="text.secondary">
                  완료 일시: {new Date(mockOrder.completed_at).toLocaleString('ko-KR')}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

