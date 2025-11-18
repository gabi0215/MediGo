import { useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActionArea,
  Chip,
  Grid,
  Button,
} from '@mui/material'
import AddIcon from '@mui/icons-material/Add'

// 임시 데이터
const mockOrders = [
  {
    id: 1,
    status: 'completed',
    created_at: '2024-01-15T10:30:00',
    delivery_address: '서울시 강남구 테헤란로 123',
    total_price: 15000,
  },
  {
    id: 2,
    status: 'delivering',
    created_at: '2024-01-16T14:20:00',
    delivery_address: '서울시 강남구 역삼동 456',
    total_price: null,
  },
  {
    id: 3,
    status: 'processing',
    created_at: '2024-01-16T16:00:00',
    delivery_address: '서울시 강남구 선릉로 789',
    total_price: null,
  },
]

const statusMap: Record<string, { label: string; color: any }> = {
  submitted: { label: '접수 완료', color: 'info' },
  processing: { label: '조제 중', color: 'warning' },
  delivering: { label: '배달 중', color: 'primary' },
  completed: { label: '배달 완료', color: 'success' },
  cancelled: { label: '취소됨', color: 'error' },
}

export default function OrderListPage() {
  const navigate = useNavigate()

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" fontWeight={600}>
          주문 내역
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/order')}
        >
          새 주문
        </Button>
      </Box>

      <Grid container spacing={2}>
        {mockOrders.map((order) => (
          <Grid item xs={12} key={order.id}>
            <Card>
              <CardActionArea onClick={() => navigate(`/orders/${order.id}`)}>
                <CardContent>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      mb: 1,
                    }}
                  >
                    <Typography variant="h6">주문 #{order.id}</Typography>
                    <Chip
                      label={statusMap[order.status].label}
                      color={statusMap[order.status].color}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {new Date(order.created_at).toLocaleString('ko-KR')}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    배달 주소: {order.delivery_address}
                  </Typography>
                  {order.total_price && (
                    <Typography variant="body2" fontWeight={600} sx={{ mt: 1 }}>
                      총 금액: {order.total_price.toLocaleString()}원
                    </Typography>
                  )}
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>

      {mockOrders.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            주문 내역이 없습니다
          </Typography>
          <Button
            variant="contained"
            onClick={() => navigate('/order')}
            sx={{ mt: 2 }}
          >
            첫 주문하기
          </Button>
        </Box>
      )}
    </Box>
  )
}

