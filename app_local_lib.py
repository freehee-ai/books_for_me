import streamlit as st
import pandas as pd
import requests

# 초기 메시지
st.text('도서를 찾고 싶은 지역을 선택해 주세요.')

# CSV 파일 로드 (로컬 파일 경로로 수정 필요)
try:
    df = pd.read_csv("C:\Users\406\Documents\GitHub\books_for_me\지역코드.csv")  
except FileNotFoundError:
    st.error("'local_books.csv' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요!")
    st.stop()

# 인증키 입력
AUTH_KEY = "password"

# ISBN 입력
isbn = ""


# 세션 스테이트 초기화
if 'residence' not in st.session_state:
    st.session_state.residence = {}

# === 전국 시/도 목록 ===
sido_list = [
    "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시",
    "대전광역시", "울산광역시", "세종특별자치시", "경기도", "강원도",
    "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"
]

# === 전국 구/군 데이터 (딕셔너리) ===
gu_dict = {
    "서울특별시": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구",
                  "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구",
                  "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구",
                  "종로구", "중구", "중랑구"],
    "부산광역시": ["강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구",
                  "사상구", "사하구", "서구", "수영구", "중구", "해운대구", "연제구", "영도구"],
    "대구광역시": ["남구", "달서구", "달성군", "동구", "북구", "서구", "수성구", "중구"],
    "인천광역시": ["계양구", "남동구", "동구", "부평구", "서구", "연수구", "중구", "강화군",
                  "옹진군", "미추홀구"],
    "광주광역시": ["광산구", "남구", "동구", "북구", "서구"],
    "대전광역시": ["대덕구", "동구", "서구", "유성구", "중구"],
    "울산광역시": ["남구", "동구", "북구", "중구", "울주군"],
    "세종특별자치시": ["세종시"],
    "경기도": ["고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시",
              "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시",
              "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시",
              "이천시", "파주시", "평택시", "포천시", "하남시", "화성시", "남부출장소"],
    "강원도": ["강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군",
              "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군",
              "횡성군", "원주시"],
    "충청북도": ["청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "진천군", "괴산군", "단양군"],
    "충청남도": ["공주시", "논산시", "계룡시", "서산시", "아산시", "천안시", "금산군", "당진시",
                "부여군", "서천군", "청양군", "태안군", "예산군", "추성군", "홍성군", "보령시"],
    "전라북도": ["전주시", "군산시", "김제시", "남원시", "익산시", "부안군", "순창군", "완주군",
                "임실군", "무주군", "장수군", "진안군", "고창군", "익산시"],
    "전라남도": ["광양시", "나주시", "목포시", "여수시", "순천시", "군산시", "고흥군", "곡성군",
                "구례군", "담양군", "무안군", "보성군", "신안군", "영광군", "영암군", "완도군",
                "장흥군", "진도군", "함평군", "해남군", "화순군", "강진군"],
    "경상북도": ["경산시", "경주시", "구미시", "김천시", "문경시", "봉화군", "상주시", "성주군",
                "안동시", "영주시", "영양군", "예천군", "울릉군", "울진군", "이천시", "청송군",
                "청양군", "포항시", "고령군", "군위군", "김천시", "칠곡군", "예천군"],
    "경상남도": ["거제시", "김해시", "마산시", "밀양시", "사천시", "양산시", "진주시", "진해구",
                "창원시", "통영시", "거창군", "고성군", "남해군", "산청군", "의령군", "창녕군",
                "하동군", "함안군", "함양군", "합천군"],
    "제주특별자치도": ["제주시", "서귀포시"]
}

# === UI 구현 ===
col1, col2 = st.columns([1, 2])

with col1:
    # 1단계: 시/도 선택
    selected_sido = st.selectbox("시/도", ["선택하세요"] + sido_list, key="sido")

with col2:
    # 2단계: 구/군 선택 (동적)
    gu_options = gu_dict.get(selected_sido, ["선택하세요"])
    selected_gu = st.selectbox("구/군", ["선택하세요"] + gu_options, key="gu")

# === 저장 및 변수 처리 ===
if st.button("도서관 찾기", type="primary"):
    if selected_sido != "선택하세요" and selected_gu != "선택하세요":
        # 선택된 값을 변수에 저장
        st.session_state.residence = {
            "sido": selected_sido,
            "gu": selected_gu,
            "full_address": f"{selected_sido} {selected_gu}"
        }

        st.success(f" {st.session_state.residence['full_address']} 선택됨!")

        # CSV에서 매핑
        matched_rows = df[
            (df['시도'] == selected_sido) & (df['구군'] == selected_gu)
        ]

        if not matched_rows.empty:
            # 같은 행의 다른 컬럼 값 출력
            st.write("지역코드와 세부지역코드")

            # API 호출 결과 저장
            api_results = []


            for index, row in matched_rows.iterrows():
                region = row['지역코드']
                dtl_region = row['세부지역코드']
            
                if not AUTH_KEY or not isbn or len(isbn) != 13 or not isbn.isdigit():
                    st.error("인증오류")
                    continue


                # API 호출 (JSON 형식)
                API_URL = "http://data4library.kr/api/libSrchByBook"
                params = {
                    "authKey": AUTH_KEY,
                    "isbn": isbn,
                    "region": region,
                    "dtl_region": dtl_region,
                    "pageNo": 1,
                    "pageSize": 50,  # 최대 100까지 가능
                    "format": "json"  # JSON 형식 지정
                }

                with st.spinner(f"🔍 도서를 보유한 도서관 찾는 중..."):
                    try:
                        response = requests.get(API_URL, params=params)
                        response.raise_for_status()
                        data = response.json()

                        # 응답 구조 확인 (매뉴얼 기반)
                        if "response" in data and "libs" in data["response"]:
                            libs = data["response"]["libs"]["lib"]
                            total_count = data["response"].get("numFound", 0)


                            if libs:
                                api_results.append({
                                    'region': region,
                                    'dtl_region': dtl_region,
                                    'total_count': total_count,
                                    'libraries': libs
                                })
                                st.success(f"✅ {region}-{dtl_region}: {len(libs)}개 도서관 소장")

                                # 도서관 목록 표 출력
                                lib_df = pd.DataFrame(libs)
                                st.dataframe(lib_df[['libCode', 'libName', 'address', 'tel']], use_container_width=True)
                            else:
                                st.warning(f"⚠️ {region}-{dtl_region}: 소장 도서관 없음")
                        else:
                            st.error(f"❌ API 응답 오류 ({region}-{dtl_region}): {data}")

                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ API 호출 실패 ({region}-{dtl_region}): {e}")
                    except ValueError as e:
                        st.error(f"❌ JSON 파싱 오류 ({region}-{dtl_region}): {e}")

            # 전체 결과 요약
            if api_results:
                st.subheader("📊 API 호출 요약")
                summary_df = pd.DataFrame([
                    {'지역코드': r['region'], '세부지역코드': r['dtl_region'], '소장 도서관 수': len(r['libraries'])}
                    for r in api_results
                ])
                st.dataframe(summary_df)

        else:
            st.warning("⚠️ 해당 지역에 CSV 데이터가 없습니다.")

    else:
        st.error("❌ 시/도와 구/군을 모두 선택해주세요!")

# === 선택된 지역 확인 ===
if 'residence' in st.session_state:
    st.info(f"**🎯 선택된 지역:** {st.session_state.residence['full_address']}")

        else:
            st.warning("해당 지역에 일치하는 도서 정보가 없습니다.")





    else:
        st.error("시/도와 구/군을 모두 선택해주세요")




