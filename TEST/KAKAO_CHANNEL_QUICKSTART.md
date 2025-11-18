# 🚀 카카오톡 채널 빠른 시작 가이드

메디-고에서 카카오톡 채널을 통해 복약 지도를 발송하는 가장 빠른 방법을 안내합니다.

## 📋 사전 준비 체크리스트

- [ ] 카카오톡 채널 생성
- [ ] 카카오 디벨로퍼스 앱 등록
- [ ] REST API 키 발급
- [ ] Admin 키 발급
- [ ] 채널 프로필 ID 확인

## ⚡ 5분 설정 가이드

### 1단계: 카카오톡 채널 생성 (2분)

```
1. https://center-pf.kakao.com/ 접속
2. "새 채널 만들기" 클릭
3. 채널명: 메디-고
4. 채널 URL에서 프로필 ID 확인 (예: _ZeUTxl)
```

### 2단계: 카카오 디벨로퍼스 설정 (2분)

```
1. https://developers.kakao.com/ 접속
2. 내 애플리케이션 > 앱 선택
3. 제품 설정 > 카카오톡 채널 > 채널 추가
4. 고객 관리 API 정책 동의 체크
5. 앱 설정 > 앱 키에서 REST API 키, Admin 키 복사
```

### 3단계: 환경 변수 설정 (1분)

`backend/.env` 파일에 추가:

```env
# Kakao Talk Channel
KAKAO_REST_API_KEY=복사한_REST_API_키
KAKAO_ADMIN_KEY=복사한_Admin_키
KAKAO_CHANNEL_PUBLIC_ID=_ZeUTxl
KAKAO_CHANNEL_API_URL=https://kapi.kakao.com
```

## 🎉 완료!

이제 복약 지도 작성 시 자동으로 카카오톡 채널 메시지가 발송됩니다!

## 🧪 테스트 방법

### 1. Backend 서버 실행

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

### 2. API 문서 확인

http://localhost:8000/docs → "카카오톡 채널" 섹션

### 3. 테스트 순서

```
1. 관리자로 로그인
2. 고객파일 생성 (POST /kakao/customer-file)
3. 주문 생성 (사용자 앱에서)
4. 복약 지도 작성 (POST /admin/medication-guidance)
5. 카카오톡에서 메시지 확인
```

## 📱 실제 메시지 발송 설정 (선택사항)

현재는 콘솔에만 출력됩니다. 실제 메시지 발송을 원하면:

### 1. 메시지 템플릿 등록

```
1. https://center-pf.kakao.com/ 접속
2. 메시지 > 메시지 설정
3. "새 템플릿 만들기"
4. 템플릿 코드 저장 (예: MEDICATION_GUIDANCE)
```

### 2. 발송 API 구현

`backend/app/services/kakao_channel_service.py`의 
`send_medication_guidance_message()` 함수 수정:

```python
async def send_medication_guidance_message(...):
    # 실제 카카오톡 메시지 API 호출
    url = f"{self.api_url}/v2/api/talk/memo/send"
    # ... 구현
```

## 🆘 문제 해결

### 401 Unauthorized
→ REST API 키 또는 Admin 키 확인

### 403 Forbidden
→ 고객 관리 API 정책 동의 확인
→ 채널이 앱에 연결되어 있는지 확인

### 채널을 찾을 수 없음
→ 채널 프로필 ID 확인 (앞에 `_` 포함)

## 📚 자세한 문서

- [카카오톡 채널 설정 가이드](docs/KAKAO_CHANNEL_SETUP.md) - 전체 설정 방법
- [카카오 디벨로퍼스 문서](https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api)
- [API 문서](docs/API.md) - API 엔드포인트 명세

## 💡 유용한 팁

1. **개발 단계에서는**: 콘솔 로그만으로도 충분히 테스트 가능
2. **테스트 계정**: 본인의 카카오톡으로 채널 추가 후 테스트
3. **메시지 템플릿**: 나중에 추가해도 OK (선택사항)

---

**참고**: 실제 서비스 배포 전에는 [카카오톡 채널 운영 정책](https://center-pf.kakao.com/notices)을 반드시 확인하세요!

