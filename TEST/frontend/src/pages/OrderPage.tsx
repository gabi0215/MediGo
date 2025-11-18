import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Button,
  TextField,
  Paper,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  Alert,
} from '@mui/material'
import CameraAltIcon from '@mui/icons-material/CameraAlt'
import Webcam from 'react-webcam'

const steps = ['처방전 촬영', '배달 정보 입력', '주문 확인']

export default function OrderPage() {
  const navigate = useNavigate()
  const webcamRef = useRef<Webcam>(null)
  const [activeStep, setActiveStep] = useState(0)
  const [prescriptionImage, setPrescriptionImage] = useState<string | null>(null)
  const [useCamera, setUseCamera] = useState(false)
  const [formData, setFormData] = useState({
    delivery_address: '',
    delivery_address_detail: '',
    delivery_zipcode: '',
    delivery_phone: '',
    delivery_note: '',
    payment_method: 'pay_at_door',
  })

  const handleCapture = () => {
    const imageSrc = webcamRef.current?.getScreenshot()
    if (imageSrc) {
      setPrescriptionImage(imageSrc)
      setUseCamera(false)
    }
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setPrescriptionImage(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1)
  }

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1)
  }

  const handleSubmit = async () => {
    // TODO: API 호출
    console.log('주문 제출', { prescriptionImage, ...formData })
    alert('주문이 접수되었습니다!')
    navigate('/orders')
  }

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              처방전 사진을 업로드하세요
            </Typography>

            {!prescriptionImage && !useCamera && (
              <Box sx={{ textAlign: 'center' }}>
                <input
                  accept="image/*"
                  style={{ display: 'none' }}
                  id="file-upload"
                  type="file"
                  onChange={handleFileUpload}
                />
                <label htmlFor="file-upload">
                  <Button
                    variant="outlined"
                    component="span"
                    fullWidth
                    size="large"
                    sx={{ mb: 2 }}
                  >
                    갤러리에서 선택
                  </Button>
                </label>
                <Button
                  variant="contained"
                  fullWidth
                  size="large"
                  startIcon={<CameraAltIcon />}
                  onClick={() => setUseCamera(true)}
                >
                  카메라로 촬영
                </Button>
              </Box>
            )}

            {useCamera && !prescriptionImage && (
              <Box>
                <Webcam
                  ref={webcamRef}
                  screenshotFormat="image/jpeg"
                  width="100%"
                  videoConstraints={{ facingMode: 'environment' }}
                />
                <Button
                  variant="contained"
                  fullWidth
                  onClick={handleCapture}
                  sx={{ mt: 2 }}
                >
                  촬영하기
                </Button>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => setUseCamera(false)}
                  sx={{ mt: 1 }}
                >
                  취소
                </Button>
              </Box>
            )}

            {prescriptionImage && (
              <Box>
                <img
                  src={prescriptionImage}
                  alt="처방전"
                  style={{ width: '100%', borderRadius: 8 }}
                />
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => setPrescriptionImage(null)}
                  sx={{ mt: 2 }}
                >
                  다시 촬영
                </Button>
              </Box>
            )}
          </Box>
        )

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              배달 정보를 입력하세요
            </Typography>
            <TextField
              fullWidth
              label="우편번호"
              value={formData.delivery_zipcode}
              onChange={(e) =>
                setFormData({ ...formData, delivery_zipcode: e.target.value })
              }
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="주소"
              required
              value={formData.delivery_address}
              onChange={(e) =>
                setFormData({ ...formData, delivery_address: e.target.value })
              }
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="상세 주소"
              value={formData.delivery_address_detail}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  delivery_address_detail: e.target.value,
                })
              }
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="연락처"
              required
              value={formData.delivery_phone}
              onChange={(e) =>
                setFormData({ ...formData, delivery_phone: e.target.value })
              }
              placeholder="010-1234-5678"
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="배달 메모"
              value={formData.delivery_note}
              onChange={(e) =>
                setFormData({ ...formData, delivery_note: e.target.value })
              }
              multiline
              rows={3}
              placeholder="문 앞에 놓아주세요"
            />
          </Box>
        )

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              주문 내용을 확인하세요
            </Typography>

            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  처방전 이미지
                </Typography>
                <img
                  src={prescriptionImage || ''}
                  alt="처방전"
                  style={{ width: '100%', maxHeight: 200, objectFit: 'cover', borderRadius: 8 }}
                />
              </CardContent>
            </Card>

            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  배달 주소
                </Typography>
                <Typography>
                  {formData.delivery_address} {formData.delivery_address_detail}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {formData.delivery_phone}
                </Typography>
              </CardContent>
            </Card>

            <FormControl component="fieldset" fullWidth>
              <FormLabel component="legend">결제 방법</FormLabel>
              <RadioGroup
                value={formData.payment_method}
                onChange={(e) =>
                  setFormData({ ...formData, payment_method: e.target.value })
                }
              >
                <FormControlLabel
                  value="pay_at_door"
                  control={<Radio />}
                  label="만나서 결제 (카드/현금)"
                />
                <FormControlLabel
                  value="card"
                  control={<Radio />}
                  label="카드 결제 (미지원)"
                  disabled
                />
              </RadioGroup>
            </FormControl>

            <Alert severity="info" sx={{ mt: 2 }}>
              주문 확정 후 약국 조제 및 배달까지 약 1-2시간 소요됩니다.
            </Alert>
          </Box>
        )

      default:
        return null
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight={600}>
        새 주문하기
      </Typography>

      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Paper sx={{ p: 3, mb: 3 }}>{renderStepContent(activeStep)}</Paper>

      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button disabled={activeStep === 0} onClick={handleBack}>
          이전
        </Button>
        <Box>
          <Button onClick={() => navigate('/')} sx={{ mr: 1 }}>
            취소
          </Button>
          {activeStep === steps.length - 1 ? (
            <Button variant="contained" onClick={handleSubmit}>
              주문하기
            </Button>
          ) : (
            <Button
              variant="contained"
              onClick={handleNext}
              disabled={
                (activeStep === 0 && !prescriptionImage) ||
                (activeStep === 1 &&
                  (!formData.delivery_address || !formData.delivery_phone))
              }
            >
              다음
            </Button>
          )}
        </Box>
      </Box>
    </Box>
  )
}

