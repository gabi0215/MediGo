# 카카오톡 채널 설정 가이드

메디-고 서비스에서 카카오톡 채널을 통해 복약 지도 메시지를 발송하고 고객을 관리하는 방법을 안내합니다.

참고: [카카오 디벨로퍼스 - 카카오톡 채널 REST API](https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api)

## 📋 사전 준비

### 1. 카카오톡 채널 생성

1. [카카오톡 채널 관리자센터](https://center-pf.kakao.com/) 접속
2. "새 채널 만들기" 클릭
3. 채널 정보 입력
   - 채널명: 메디-고
   - 카테고리: 의료/건강
   - 공개 설정: 공개

### 2. 카카오 디벨로퍼스 앱 설정

1. [카카오 디벨로퍼스](https://developers.kakao.com/) 접속
2. 내 애플리케이션 > 앱 선택
3. **플랫폼 설정**
   - Android/iOS 앱 패키지명 등록
   - Web 도메인 등록

4. **카카오 로그인 활성화**
   - 제품 설정 > 카카오 로그인 > 활성화

5. **동의항목 설정**
   - 제품 설정 > 카카오 로그인 > 동의항목
   - "카카오톡 채널 추가 상태" 선택 사용

6. **카카오톡 채널 연결**
   - 제품 설정 > 카카오톡 채널
   - 채널 추가 > 검색하여 연결

7. **고객 관리 API 정책 동의**
   - 제품 설정 > 카카오톡 채널 > 고객 관리 API
   - 정책 동의 체크

### 3. API 키 발급

앱 설정 > 앱 키에서 다음 정보 확인:

- **REST API 키**: 일반적인 API 호출용
- **Admin 키**: 관리자 권한이 필요한 API 호출용

### 4. 채널 프로필 ID 확인

1. [카카오톡 채널 관리자센터](https://center-pf.kakao.com/) 접속
2. 채널 선택 > 관리 > 상세정보
3. **채널 URL**에서 프로필 ID 확인
   - 예: `http://pf.kakao.com/_ZeUTxl` → `_ZeUTxl`

## 🔧 환경 변수 설정

`backend/.env` 파일에 다음 정보 추가:

```env
# Kakao Talk Channel
KAKAO_REST_API_KEY=your_rest_api_key_here
KAKAO_ADMIN_KEY=your_admin_key_here
KAKAO_CHANNEL_PUBLIC_ID=_ZeUTxl
KAKAO_CHANNEL_API_URL=https://kapi.kakao.com
```

## 📡 API 사용 방법

### 1. 채널 관계 조회

사용자가 채널을 추가했는지 확인:

```bash
curl -X GET "http://localhost:8000/api/v1/kakao/channel/relation/123" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### 2. 고객파일 생성

주문 고객 관리를 위한 고객파일 생성:

```bash
curl -X POST "http://localhost:8000/api/v1/kakao/customer-file" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "메디-고 주문 고객",
    "description": "약 배달 서비스 이용 고객",
    "schema": {
      "주문번호": "Number",
      "주문일시": "String",
      "배달주소": "String",
      "연락처": "String"
    }
  }'
```

응답:
```json
{
  "file_id": 437,
  "name": "메디-고 주문 고객",
  "status": "active"
}
```

### 3. 고객파일에 사용자 추가

주문 발생 시 고객 정보 추가:

```bash
curl -X POST "http://localhost:8000/api/v1/kakao/customer-file/add-users" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### 4. 고객파일 조회

```bash
curl -X GET "http://localhost:8000/api/v1/kakao/customer-file/437" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### 5. 고객파일에서 사용자 삭제

```bash
curl -X POST "http://localhost:8000/api/v1/kakao/customer-file/delete-users" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": 437,
    "user_type": "app",
    "user_ids": ["12345"]
  }'
```

## 💊 복약 지도 메시지 발송

### 1. 메시지 템플릿 등록 (카카오톡 채널 관리자센터)

1. [카카오톡 채널 관리자센터](https://center-pf.kakao.com/) 접속
2. 메시지 > 메시지 설정
3. "새 템플릿 만들기" 클릭
4. 템플릿 작성:

```
안녕하세요 #{name}님,
처방받으신 약이 배달 완료되었습니다. 💊

[복약 지도]
#{guidance}

건강하세요!
- 메디-고 팀
```

5. 템플릿 코드 저장 (예: `MEDICATION_GUIDANCE`)

### 2. 메시지 발송 코드

복약 지도 작성 시 자동으로 카카오톡 채널 메시지 발송:

```python
# backend/app/api/v1/endpoints/admin.py
await kakao_channel_service.send_medication_guidance_message(
    user_id=str(order.user_id),
    order_id=order.id,
    guidance_text=guidance_data.guidance_text,
)
```

## 🔒 보안 주의사항

1. **API 키 보안**
   - `.env` 파일은 절대 Git에 커밋하지 마세요
   - 프로덕션 환경에서는 환경 변수 또는 AWS Secrets Manager 사용

2. **Admin 키 사용**
   - Admin 키는 서버 측에서만 사용
   - 클라이언트에 노출 금지

3. **채널 프로필 ID**
   - 공개 정보이므로 하드코딩 가능
   - 하지만 환경 변수로 관리 권장

## 📊 고객 관리 워크플로우

### 주문 발생 시

```
1. 사용자 주문 생성
   ↓
2. 고객파일에 사용자 정보 추가
   - 주문번호, 주문일시, 배달주소 등
   ↓
3. 약국 조제 및 배달
   ↓
4. 복약 지도 작성
   ↓
5. 카카오톡 채널 메시지 발송
   - 복약 지도 내용 전달
   ↓
6. 사용자 확인
```

## 🚀 테스트 방법

### 1. 개발 환경 테스트

```bash
# Backend 서버 실행
cd backend
uvicorn app.main:app --reload

# API 테스트 (Thunder Client, Postman 등)
# 또는 Swagger UI: http://localhost:8000/docs
```

### 2. 카카오톡 채널 테스트 계정

1. 카카오톡 앱 설치
2. 메디-고 채널 검색 및 추가
3. 테스트 주문 생성
4. 메시지 수신 확인

## 🔧 트러블슈팅

### API 호출 실패

**오류**: `401 Unauthorized`

**해결**: 
- REST API 키 또는 Admin 키 확인
- 헤더 형식 확인: `Authorization: KakaoAK ${API_KEY}`

---

**오류**: `403 Forbidden`

**해결**:
- 고객 관리 API 정책 동의 확인
- 채널이 앱에 연결되어 있는지 확인

---

**오류**: `400 Bad Request - invalid channel_public_id`

**해결**:
- 채널 프로필 ID 확인 (앞에 `_` 포함)
- 채널이 공개 상태인지 확인

### 메시지 발송 안 됨

1. 메시지 템플릿이 등록되어 있는지 확인
2. 템플릿이 승인되었는지 확인
3. 사용자가 채널을 추가했는지 확인

## 📚 참고 자료

- [카카오톡 채널 REST API 문서](https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api)
- [카카오톡 채널 관리자센터](https://center-pf.kakao.com/)
- [카카오 디벨로퍼스](https://developers.kakao.com/)
- [카카오톡 메시지 템플릿 가이드](https://developers.kakao.com/docs/latest/ko/message/message-template)

## ⚠️ 주의사항

1. **쿼터 제한**
   - API 호출 횟수 제한이 있습니다
   - [카카오 디벨로퍼스 - 쿼터](https://developers.kakao.com/docs/latest/ko/getting-started/quota) 참조

2. **개인정보 처리**
   - 고객 정보는 개인정보보호법에 따라 처리
   - 30일 이상 미사용 고객 정보는 삭제 권장

3. **메시지 발송 규정**
   - 광고성 메시지는 사전 동의 필수
   - 야간 시간(21:00-08:00) 발송 제한

