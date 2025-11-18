# 메디-고 API 문서

Base URL: `http://localhost:8000/api/v1`

## 인증

JWT Bearer 토큰 사용

```
Authorization: Bearer {access_token}
```

---

## 인증 (Auth)

### POST /auth/kakao
카카오 OAuth 로그인

**Request Body:**
```json
{
  "access_token": "kakao_access_token"
}
```

**Response:**
```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "token_type": "bearer"
}
```

### POST /auth/refresh
토큰 갱신

**Request Body:**
```json
{
  "refresh_token": "jwt_refresh_token"
}
```

---

## 사용자 (Users)

### GET /users/me
내 프로필 조회

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "홍길동",
  "phone": "010-1234-5678",
  "delivery_address": "서울시 강남구...",
  "kakao_profile_image": "https://..."
}
```

### PUT /users/me
내 프로필 수정

**Request Body:**
```json
{
  "full_name": "홍길동",
  "phone": "010-1234-5678",
  "delivery_address": "서울시 강남구...",
  "delivery_address_detail": "101동 1001호",
  "delivery_zipcode": "12345"
}
```

---

## 주문 (Orders)

### POST /orders
주문 생성

**Request Body:**
```json
{
  "prescription_image_base64": "base64_encoded_image",
  "delivery_address": "서울시 강남구...",
  "delivery_address_detail": "101동 1001호",
  "delivery_zipcode": "12345",
  "delivery_phone": "010-1234-5678",
  "delivery_note": "문 앞에 놓아주세요",
  "payment_method": "pay_at_door"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "status": "submitted",
  "delivery_address": "서울시 강남구...",
  "created_at": "2024-01-15T10:30:00"
}
```

### GET /orders
내 주문 목록

**Query Parameters:**
- `skip`: 페이징 오프셋 (기본값: 0)
- `limit`: 페이지 크기 (기본값: 20)

### GET /orders/{order_id}
주문 상세 조회

### GET /orders/{order_id}/status
주문 상태 조회

**Response:**
```json
{
  "order_id": 1,
  "status": "processing",
  "status_message": "약국에서 조제 중입니다.",
  "updated_at": "2024-01-15T10:35:00"
}
```

---

## 관리자 (Admin)

모든 엔드포인트는 관리자 권한 필요

### GET /admin/orders
전체 주문 목록

**Query Parameters:**
- `status`: 주문 상태 필터 (submitted, processing, delivering, completed, cancelled)
- `skip`: 페이징 오프셋
- `limit`: 페이지 크기

### PUT /admin/orders/{order_id}
주문 정보 수정

**Request Body:**
```json
{
  "status": "processing",
  "medicine_price": 12000,
  "delivery_fee": 3000,
  "is_paid": true,
  "admin_note": "조제 완료",
  "pharmacy_name": "행복약국"
}
```

### POST /admin/orders/{order_id}/medicine-bag
약봉투 사진 업로드

**Request Body:**
```json
{
  "base64_image": "base64_encoded_image"
}
```

### POST /admin/medication-guidance
복약 지도 작성 및 발송

**Request Body:**
```json
{
  "order_id": 1,
  "guidance_text": "김지수님, 처방받으신 약은...",
  "is_ai_generated": false,
  "ai_model_version": null
}
```

### GET /admin/orders/{order_id}/medication-guidance
복약 지도 조회

---

## 카카오톡 채널 (Kakao Channel)

모든 엔드포인트는 관리자 권한 필요

### GET /kakao/channel/relation/{user_id}
카카오톡 채널 관계 조회

**Response:**
```json
{
  "channels": [
    {
      "channel_uuid": "...",
      "channel_public_id": "_ZeUTxl",
      "relation": "added"
    }
  ]
}
```

### POST /kakao/customer-file
고객파일 생성

**Request Body:**
```json
{
  "name": "메디-고 주문 고객",
  "description": "약 배달 서비스 이용 고객",
  "schema": {
    "주문번호": "Number",
    "주문일시": "String",
    "배달주소": "String",
    "연락처": "String"
  }
}
```

**Response:**
```json
{
  "file_id": 437,
  "name": "메디-고 주문 고객",
  "status": "active"
}
```

### GET /kakao/customer-file/{file_id}
고객파일 조회

### POST /kakao/customer-file/add-users
고객파일에 사용자 추가

**Request Body:**
```json
{
  "file_id": 437,
  "user_type": "app",
  "users": [
    {
      "id": "12345",
      "field": {
        "주문번호": 100,
        "주문일시": "2024-01-16 10:30:00",
        "배달주소": "서울시 강남구 테헤란로 123",
        "연락처": "010-1234-5678"
      }
    }
  ]
}
```

**Response:**
```json
{
  "file_id": 437,
  "request_count": 1,
  "success_count": 1
}
```

### POST /kakao/customer-file/delete-users
고객파일에서 사용자 삭제

**Request Body:**
```json
{
  "file_id": 437,
  "user_type": "app",
  "user_ids": ["12345"]
}
```

---

## 주문 상태 (Order Status)

- `submitted`: 접수 완료
- `processing`: 약국 조제 중
- `delivering`: 배달 중
- `completed`: 배달 완료
- `cancelled`: 취소

## 결제 방법 (Payment Method)

- `pay_at_door`: 만나서 결제
- `card`: 카드 결제 (향후 지원)
- `cash`: 현금

## 에러 코드

- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `404`: 리소스를 찾을 수 없음
- `500`: 서버 오류

