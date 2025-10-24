import pandas as pd
import numpy as np
import streamlit as st
import os
import zipfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Streamlit 설정
st.set_page_config(page_title="도서 추천 시스템", layout="wide")

# 데이터 폴더 경로
data_dir = './data/인기대출도서'

# Streamlit UI
st.title("📚 선택 도서 기반 유사도 추천 시스템")
st.write("성별과 연령대를 선택하고 여러 도서를 선택하면, 비슷한 도서를 추천합니다.")

# 사용자 입력
age = ['선택 없음', '10대이하', '2030대', '4050대', '60대이상']
gender = ['선택 없음', '여성', '남성']

age = st.selectbox('연령대를 선택하세요:', age)
gender = st.selectbox('성별을 선택하세요:', gender)

# 한글 파일명 구조
filename = f"BestLoanList_{gender}_{age}.csv"
filepath = os.path.join(data_dir, filename)
print(filepath)


# 파일 존재 확인
if not os.path.exists(filepath):
    st.stop()

# CSV 파일 로드
df = pd.read_csv(filepath, encoding='cp949')

# 주요 컬럼 자동 탐색
col_title = next((c for c in df.columns if '서명' in c or 'TITLE' in c), None)
col_author = next((c for c in df.columns if '저자' in c or 'AUTHOR' in c), None)

if not col_title:
    st.error("도서 제목(서명) 컬럼을 찾을 수 없습니다.")
    st.stop()

# 중복 제거 및 선택 UI
df = df.drop_duplicates(subset=col_title, ignore_index=True)
st.subheader(f"📘 {gender} {age} 인기 도서 목록")
selected_books = st.multiselect('도서를 선택하세요 (최대 5개):', 
                                df[col_title].dropna().unique(), max_selections=5)

# 사용자가 책을 선택한 경우
if selected_books:
    # 텍스트 결합
    df['text'] = ''
    if col_author:
        df['text'] += df[col_author].fillna('') + ' '
    df['text'] += df[col_title].fillna('')

    if df['text'].str.strip().eq('').all():
        df['text'] = df[col_title].fillna('')

    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df['text'])

    # 선택한 도서들의 벡터 평균 계산
    selected_indices = [df[df[col_title] == book].index[0] for book in selected_books]
    mean_vector = tfidf_matrix[selected_indices].mean(axis=0)
    mean_vector = np.asarray(mean_vector)

    # 전체 도서와의 코사인 유사도 계산
    sim_scores = cosine_similarity(mean_vector, tfidf_matrix).flatten()

    # 선택한 책 제외 후 상위 5개 출력
    recommendations = [(i, score) for i, score in enumerate(sim_scores) 
                       if df.loc[i, col_title] not in selected_books]
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:5]

    st.markdown("---")
    st.subheader("✨ 선택한 도서들과 유사한 도서 추천")

    for rank, (i, score) in enumerate(recommendations, start=1):
        images = pd.read_csv('./data/book_image.zip', compression='zip')
        with zipfile.ZipFile('./data/book_image.zip', 'r') as z:
            print(z.namelist())

        url = images['IMAGE_URL']
        title = df.loc[i, col_title]
        author = df.loc[i, col_author] if col_author else "저자 정보 없음"
        match = images[images['책이름'].str.strip() == str(title).strip()]
        st.write(f"{rank}. {title} ({author})")
        if not match.empty:
            image_url = match.iloc[0]['IMAGE_URL']
            # 이미지와 제목, 저자 표시
            st.image(image_url, caption=f"{rank}. {title} ({author})", width=150)
        else:
            # 이미지가 없을 경우 텍스트로만 표시
            st.write(" - 이미지 없음")
else:
    st.info("최소 1권 이상의 책을 선택하세요 👆")
