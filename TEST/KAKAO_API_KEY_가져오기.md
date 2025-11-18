# 🔑 카카오 API 키 발급받기

채널 정보는 확인했습니다! 이제 **카카오 디벨로퍼스에서 API 키**를 발급받아야 합니다.

## ✅ 확인된 정보 (예시)

- 채널 이름: **[귀하의 채널명]**
- 검색용 ID: **[귀하의 검색용 ID]**
- 채널 프로필 ID: **_XXXXXX** (카카오톡 채널 관리자센터에서 확인)
- 채널 URL: http://pf.kakao.com/_XXXXXX

## 🔑 추가로 필요한 정보 (필수!)

### 1️⃣ 카카오 디벨로퍼스 앱 등록

#### Step 1: 앱 생성
1. [카카오 디벨로퍼스](https://developers.kakao.com/) 접속
2. 로그인 (카카오 계정)
3. **상단 메뉴 > 내 애플리케이션** 클릭
4. **애플리케이션 추가하기** 클릭
5. 앱 정보 입력:
   ```
   앱 이름: [귀하의 앱 이름]
   사업자명: (본인 이름 또는 사업자명)
   ```

#### Step 2: REST API 키 복사
```
내 애플리케이션 > 앱 선택 > 앱 설정 > 앱 키
```

여기서 다음 두 개의 키를 복사하세요:

**📝 복사할 키:**
- **REST API 키**: `abc123def456...` (예시)
- **Admin 키**: `xyz789uvw012...` (예시)

### 2️⃣ 카카오톡 채널 연결

#### Step 1: 제품 설정
```
내 애플리케이션 > 앱 선택 > 제품 설정 > 카카오톡 채널
```

#### Step 2: 채널 추가
1. **카카오톡 채널 추가하기** 클릭
2. **검색** 탭에서 `귀하의 채널명` 검색
3. 채널 선택 후 **추가** 클릭

✅ 연결 완료 확인: 채널 목록에 귀하의 채널 표시

### 3️⃣ 고객 관리 API 정책 동의 (중요!)

```
내 애플리케이션 > 앱 선택 > 제품 설정 > 카카오톡 채널
```

하단의 **고객 관리 API** 섹션에서:
- ☑️ **정책 동의** 체크박스 클릭
- 약관 읽고 동의

⚠️ 이 단계를 빠뜨리면 API 호출 시 403 에러 발생!

### 4️⃣ 플랫폼 등록 (선택사항 - 로그인 기능 사용 시)

```
내 애플리케이션 > 앱 선택 > 앱 설정 > 플랫폼
```

**Web 플랫폼 추가:**
```
사이트 도메인: http://localhost:3000
```

**Android 추가 (향후 앱 개발 시):**
```
패키지명: com.medigo.app
```

## 📝 .env 파일 설정

API 키를 발급받으면 `backend/.env` 파일에 입력:

```env
# Kakao Talk Channel
KAKAO_REST_API_KEY=여기에_발급받은_REST_API_키_붙여넣기
KAKAO_ADMIN_KEY=여기에_발급받은_Admin_키_붙여넣기
KAKAO_CHANNEL_PUBLIC_ID=_XXXXXX
KAKAO_CHANNEL_API_URL=https://kapi.kakao.com
```

### 예시:
```env
KAKAO_REST_API_KEY=여기에_REST_API_키_기입
KAKAO_ADMIN_KEY=여기에_Admin_키_기입
KAKAO_CHANNEL_PUBLIC_ID=여기에_채널_프로필_ID_기입
KAKAO_CHANNEL_API_URL=https://kapi.kakao.com
```

## ✅ 완료 체크리스트

설정이 완료되면 다음을 확인하세요:

- [ ] 카카오 디벨로퍼스 앱 생성 완료
- [ ] REST API 키 발급 완료
- [ ] Admin 키 확인 완료
- [ ] 카카오톡 채널 연결 완료
- [ ] 고객 관리 API 정책 동의 완료
- [ ] `backend/.env` 파일에 키 입력 완료

## 🧪 테스트 방법

모든 설정이 완료되면:

```bash
# 1. Backend 서버 실행
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload

# 2. API 테스트
# http://localhost:8000/docs 접속
# "카카오톡 채널" 섹션에서 API 테스트
```

### 테스트 API 호출:

```bash
# 채널 관계 조회 테스트
curl -X GET "http://localhost:8000/api/v1/kakao/channel/relation/1" \
  -H "Authorization: Bearer {관리자_토큰}"
```

성공하면 채널 정보가 반환됩니다! 🎉

## 🆘 문제 발생 시

### 401 Unauthorized
→ REST API 키가 올바른지 확인
→ `.env` 파일 저장 후 서버 재시작

### 403 Forbidden
→ 고객 관리 API 정책 동의 확인
→ 채널이 앱에 연결되어 있는지 확인

### 404 Not Found
→ 채널 프로필 ID 확인
→ 채널이 공개 상태인지 확인

## 📞 도움이 필요하면

1. [카카오 디벨로퍼스 FAQ](https://developers.kakao.com/docs/latest/ko/getting-started/faq)
2. [카카오톡 채널 관리자센터](https://center-pf.kakao.com/)
3. DevTalk (카카오 개발자 포럼)

---

**다음 단계**: API 키를 발급받아 `.env` 파일에 입력하세요!

