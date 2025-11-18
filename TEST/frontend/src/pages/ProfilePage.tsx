import { useState } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Avatar,
  TextField,
  Button,
  Divider,
} from '@mui/material'
import { useAuthStore } from '../stores/authStore'

export default function ProfilePage() {
  const { user } = useAuthStore()
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    phone: '',
    delivery_address: '',
    delivery_address_detail: '',
    delivery_zipcode: '',
  })

  const handleSave = () => {
    // TODO: API 호출하여 프로필 업데이트
    console.log('프로필 저장', formData)
    setIsEditing(false)
    alert('프로필이 저장되었습니다')
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight={600}>
        내 프로필
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent sx={{ textAlign: 'center', py: 4 }}>
          <Avatar
            alt={user?.full_name || '사용자'}
            src={user?.kakao_profile_image || ''}
            sx={{ width: 100, height: 100, mx: 'auto', mb: 2 }}
          />
          <Typography variant="h6">{user?.full_name || '사용자'}</Typography>
          <Typography variant="body2" color="text.secondary">
            {user?.email || '이메일 없음'}
          </Typography>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h6">개인 정보</Typography>
            <Button
              variant={isEditing ? 'contained' : 'outlined'}
              onClick={() => {
                if (isEditing) {
                  handleSave()
                } else {
                  setIsEditing(true)
                }
              }}
            >
              {isEditing ? '저장' : '수정'}
            </Button>
          </Box>
          <Divider sx={{ mb: 3 }} />

          <TextField
            fullWidth
            label="이름"
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            disabled={!isEditing}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="전화번호"
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            disabled={!isEditing}
            sx={{ mb: 2 }}
            placeholder="010-1234-5678"
          />
          <TextField
            fullWidth
            label="우편번호"
            value={formData.delivery_zipcode}
            onChange={(e) => setFormData({ ...formData, delivery_zipcode: e.target.value })}
            disabled={!isEditing}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="주소"
            value={formData.delivery_address}
            onChange={(e) => setFormData({ ...formData, delivery_address: e.target.value })}
            disabled={!isEditing}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="상세 주소"
            value={formData.delivery_address_detail}
            onChange={(e) =>
              setFormData({ ...formData, delivery_address_detail: e.target.value })
            }
            disabled={!isEditing}
          />

          {isEditing && (
            <Button
              fullWidth
              variant="outlined"
              onClick={() => setIsEditing(false)}
              sx={{ mt: 2 }}
            >
              취소
            </Button>
          )}
        </CardContent>
      </Card>
    </Box>
  )
}

