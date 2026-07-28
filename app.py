import streamlit as st
import json
from google import genai
from google.genai import types

# 1. 보안 설정: Streamlit Secrets로부터 무료 Gemini API 키 로드
if "GEMINI_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GOOGLE_API_KEY)
else:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 화면 레이아웃 설정
st.set_page_config(page_title="RFP 기반 전략 TOC 생성기", layout="wide")
st.title("💡 NEXUS 컨설팅 - 전략 제안서 TOC 생성 시스템")
st.caption("무료 Gemini API와 Few-Shot Learning을 활용한 브랜드 맞춤형 초안 빌더")

# 세션 상태 초기화 (버튼 클릭 시 데이터 보존용)
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = None

# 상단: 1단계 RFP 입력 섹션
st.subheader("1단계: 날것의 RFP(제안요청서) 원문 입력")
rfp_input = st.text_area(
    "고객사로부터 받은 RFP나 프로젝트 요구사항을 그대로 붙여넣으세요.",
    height=150,
    placeholder="예시: 이번에 우리 기업에서 임직원용 AI 챗봇 인프라를 도입하려고 합니다. 예산은 5천만 원이며 보안이 가장 중요합니다. 개발 기간은 3달입니다. 생성형 AI 기술을 활용해 인사 가이드를 자동화하는 것이 핵심입니다."
)

# 1차 분석 버튼
if st.button("RFP 구조화 분석 시작 🔍"):
    if not rfp_input.strip():
        st.warning("RFP 내용을 입력해주세요.")
    else:
        with st.spinner("RFP에서 핵심 정보를 구조화하는 중..."):
            # 1차 파싱을 위한 시스템 프롬프트 (JSON 강제)
            parser_prompt = f"""
            너는 입력된 RFP 원문에서 핵심 제안 요소를 추출하는 데이터 파서(Parser)야.
            입력된 텍스트를 분석하여 반드시 아래의 JSON 포맷으로만 답변해줘. 다른 설명 텍스트는 절대 붙이지 마.

            {{
              "audience": "최종 보고를 받고 의사결정을 내릴 청자 (예: 공공기관 평가위원, C-Level 등)",
              "product_service": "제안해야 하는 핵심 상품 또는 핵심 솔루션 기술명",
              "mandatory_elements": "반드시 포함해야 하는 규격, 필수 기능, 제약 사항들 (쉼표로 구분)",
              "resources": "제안사가 보유한 핵심 기술력, 인력, 예산 등 활용 가능한 자원 (쉼표로 구분)"
            }}

            [RFP 원문]
            {rfp_input}
            """
            
            # 최신 구글 공식 추천 모델인 gemini-2.5-flash 사용
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=parser_prompt,
            )
            
            try:
                cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
                st.session_state.parsed_data = json.loads(cleaned_text)
            except Exception as e:
                st.error("AI 응답을 JSON으로 파싱하는 데 실패했습니다. 다시 시도해 주세요.")

# 2단계: 구조화된 데이터 시각화 및 사용자의 직접 수정(Tuning) 섹션
if st.session_state.parsed_data:
    st.markdown("---")
    st.subheader("2단계: 구조화 데이터 확인 및 검증 (수정 가능)")
    st.info("AI가 추출한 정보입니다. 어색한 부분은 직접 타이핑하여 수정한 뒤 하단의 생성 버튼을 누르세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        audience = st.text_input("🎯 보고 청자 / 타겟", value=st.session_state.parsed_data.get("audience", ""))
        product_service = st.text_input("💻 제안 핵심 솔루션", value=st.session_state.parsed_data.get("product_service", ""))
    with col2:
        mandatory_elements = st.text_area("⚠️ 필수 포함 요소", value=st.session_state.parsed_data.get("mandatory_elements", ""), height=68)
        resources = st.text_area("🛠️ 활용 리소스 / 예산", value=st.session_state.parsed_data.get("resources", ""), height=68)

    # 3단계: 백단 컨텍스트(브랜드 핏) 조립 및 최종 생성
    if st.button("브랜드 맞춤형 TOC & Key Idea 초안 생성 🚀"):
        with st.spinner("NEXUS 컨설팅 스타일로 목차를 빌드하는 중..."):
            
            nexus_brand_context = """
            [System Context]
            너는 대한민국 최고의 IT 전략 컨설팅 펌인 'NEXUS 컨설팅'의 대표 파트너다. 
            우리 브랜드는 항상 직관적이고, 데이터 기반의 솔루션을 제시하며, 모든 목차의 끝은 '명사형 종결'로 끝나는 핏(Fit)을 가지고 있다. 
            
            아래는 우리 NEXUS 브랜드가 수주에 성공했던 실제 우수 제안서의 TOC 패턴과 Key Idea 샘플이다. 이 스타일, 깊이, 위계를 완벽하게 모방해라.

            ---
            ■ NEXUS 우수 성공 샘플 1 (엔터프라이즈 DX 제안서)
            - 청자: 제조 대기업 C-Level 및 DX 추진 단장
            - 솔루션: 클라우드 기반 스마트 팩토리 인프라
            - 필수요소: 24시간 무중단 가동, 데이터 보안 가이드라인 준수
            - 리소스: 사내 인프라 아키텍트 5명, 2억 원 예산
            [출력 TOC]
            Ⅰ. 글로벌 제조 혁신을 위한 스마트 인프라 도입 개요
              1. 국내외 스마트 팩토리 표준 동향 및 시사점
              2. 레거시 생산 설비의 데이터 병목 현상 분석
            Ⅱ. NEXUS 클라우드 기반 무중단 아키텍처 설계 방안
              1. 24/7 다운타임 제로 구현을 위한 이중화 인프라 구성
              2. 공장 데이터 보안 가이드라인 완벽 대응 시나리오
            Ⅲ. 안정적 마이그레이션을 위한 투입 인력 및 일정 계획
              1. 특급 아키텍트 중심의 단계별 리스크 관리 방안
            [Key Idea]
            "단순한 서버 이설이 아닌, 다운타임 제로(Zero)를 달성하여 제조 효율성을 240% 극대화하는 인프라 혁신"
            ---
            """

            final_prompt = f"""
            {nexus_brand_context}

            [User Data (현재 진행할 제안 요청 정보)]
            - 청자: {audience}
            - 솔루션: {product_service}
            - 필수요소: {mandatory_elements}
            - 리소스: {resources}

            [출력 지침]
            위의 'NEXUS 우수 성공 샘플'의 구조, 톤앤매너, 명사형 종결 규칙을 100% 반영하여, 이번 User Data에 최적화된 새로운 [TOC]와 [Key Idea] 초안을 생성해줘. 다른 잡담은 하지 말고 결과만 출력해줘.
            """

            # 최신 구글 공식 추천 모델 호출 방식으로 2차 빌드 진행
            final_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=final_prompt,
            )
            
            st.markdown("---")
            st.subheader("📝 최종 결과물: NEXUS 브랜드 맞춤형 초안")
            st.code(final_response.text, language="markdown")
            st.success("초안 생성이 완료되었습니다! 위 박스 우측 상단 버튼을 눌러 복사(Copy)하세요.")
