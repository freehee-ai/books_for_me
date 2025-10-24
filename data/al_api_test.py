import urllib.request  # 인터넷에서 URL로 데이터를 요청하기 위한 모듈
import urllib.parse   # URL 파라미터를 인코딩하기 위한 모듈
import json           # JSON 데이터를 처리하기 위한 모듈

def fetch_aladin_item_lookup(ttb_key, item_id, item_id_type='ISBN13', output='JS', version='20131101', opt_result='ebookList,usedList,reviewList'):
    """
    알라딘 ItemLookUp API를 사용해 상품 정보를 JSON 형식으로 가져옵니다.
    
    매개변수:
    - ttb_key: 알라딘에서 발급받은 TTBKey (필수)
    - item_id: 조회하려는 상품의 ID (예: ISBN13)
    - item_id_type: 'ISBN' 또는 'ISBN13' (기본값: 'ISBN13')
    - output: 응답 형식, 'XML' 또는 'JS'(JSON) (기본값: 'JS')
    - version: API 버전 (기본값: '20131101')
    - opt_result: 추가 정보 (기본값: 'ebookList,usedList,reviewList')
    
    반환값:
    - JSON 응답인 경우 Python 딕셔너리, 실패 시 None
    """
    # 알라딘 ItemLookUp API의 기본 URL
    base_url = 'http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx'
    
    # API 요청에 필요한 파라미터를 딕셔너리로 정의
    params = {
        'ttbkey': ttb_key,
        'ItemId': item_id,
        'ItemIdType': item_id_type,
        'output': output,
        'Version': version,
        'OptResult': opt_result
    }
    
    # 파라미터를 URL 쿼리 문자열로 변환 (예: ttbkey=abc&ItemId=123)
    query_string = urllib.parse.urlencode(params)
    # 최종 URL 생성 (기본 URL + 쿼리 문자열)
    full_url = f"{base_url}?{query_string}"
    
    try:
        # URL로 요청 보내고 응답 받기
        with urllib.request.urlopen(full_url) as response:
            # 응답 데이터를 읽고 UTF-8로 디코딩
            data = response.read().decode('utf-8')
            
            # JSON 형식으로 응답 처리
            if output.lower() == 'js':
                try:
                    # JSON 문자열을 Python 딕셔너리로 변환
                    json_data = json.loads(data)
                    return json_data
                except json.JSONDecodeError as e:
                    print(f"JSON 파싱 오류: {str(e)}")
                    return None
            else:
                print("이 코드는 JSON 응답만 처리합니다. Output=JS로 설정하세요.")
                return None
                
    except urllib.error.HTTPError as e:
        # HTTP 오류 (예: 404, 500) 처리
        print(f"HTTP 오류: {e.code} - {e.reason}")
        return None
    except urllib.error.URLError as e:
        # URL 오류 (예: 인터넷 연결 문제) 처리
        print(f"URL 오류: {e.reason}")
        return None
    except Exception as e:
        # 기타 예외 처리
        print(f"예상치 못한 오류: {str(e)}")
        return None

# 예시 사용
if __name__ == "__main__":
    # 실제 TTBKey로 교체해야 함
    ttb_key = 'ttbfreehee03271034002'  # 알라딘에서 발급받은 TTBKey 입력
    item_id = '9791159921445'      # 예시 ISBN13 (실제 ISBN13으로 교체 가능)
    
    # API 호출
    result = fetch_aladin_item_lookup(ttb_key, item_id, output='JS')
    
    if result is not None:
        # JSON 응답에서 주요 정보 추출
        try:
            # 'item' 리스트에서 첫 번째 상품 정보 가져오기
            item = result['item'][0] if 'item' in result and result['item'] else None
            
            if item:
                # 주요 필드 추출
                title = item.get('title', '정보 없음')  # 상품명
                author = item.get('author', '정보 없음')  # 저자
                price_sales = item.get('priceSales', '정보 없음')  # 판매가
                publisher = item.get('publisher', '정보 없음')  # 출판사
                pub_date = item.get('pubDate', '정보 없음')  # 출간일
                isbn13 = item.get('isbn13', '정보 없음')  # ISBN13
                
                # 정보 출력
                print("=== 상품 정보 ===")
                print(f"상품명: {title}")
                print(f"저자: {author}")
                print(f"판매가: {price_sales}원")
                print(f"출판사: {publisher}")
                print(f"출간일: {pub_date}")
                print(f"ISBN13: {isbn13}")

                # 베스트셀러 순위 정보
                best_seller_rank = item.get('bestSellerRank', '정보 없음')
                print(f"\n베스트셀러 순위: {best_seller_rank}")
                
                # 평점 정보 (ratingInfo 객체)
                rating_info = item.get('ratingInfo', {})
                rating_score = rating_info.get('ratingScore', '정보 없음')  # 실수 (별 평점)
                rating_count = rating_info.get('ratingCount', '정보 없음')  # 정수 (별 개수)
                comment_review_count = rating_info.get('commentReviewCount', '정보 없음')  # 정수 (100자평 개수)
                my_review_count = rating_info.get('myReviewCount', '정보 없음')  # 정수 (마이리뷰 개수)
                
                print("\n=== 평점 및 리뷰 정보 (ratingInfo) ===")
                print(f"별 평점: {rating_score}")
                print(f"별을 남긴 개수: {rating_count}")
                print(f"100자평 개수: {comment_review_count}")
                print(f"마이리뷰 개수: {my_review_count}")
                
                # 카드 리뷰 이미지 목록 (cardReviewImgList 배열)
                card_review_imgs = item.get('cardReviewImgList', [])
                print("\n=== 카드 리뷰 이미지 경로 (cardReviewImgList) ===")
                if card_review_imgs:
                    for i, img_url in enumerate(card_review_imgs, 1):
                        print(f"이미지 {i}: {img_url}")
                else:
                    print("카드 리뷰 이미지가 없습니다.")



                
                # 부가 정보 (예: 전자책 정보) 확인
                if 'subInfo' in item and 'ebookList' in item['subInfo']:
                    print("\n=== 전자책 정보 ===")
                    for ebook in item['subInfo']['ebookList']:
                        ebook_title = ebook.get('title', '정보 없음')
                        ebook_price = ebook.get('priceSales', '정보 없음')
                        print(f"전자책 제목: {ebook_title}")
                        print(f"전자책 가격: {ebook_price}원")
            else:
                print("상품 정보를 찾을 수 없습니다.")
                
        except KeyError as e:
            print(f"데이터 처리 중 오류: 필드 {e}가 없습니다.")
    else:
        print("데이터를 가져오지 못했습니다.")