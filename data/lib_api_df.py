import requests  # 웹 요청을 보내는 라이브러리예요.
import xmltodict  # XML을 JSON(딕셔너리)로 바꾸는 도구예요.
import pandas as pd  # DataFrame을 만들기 위한 라이브러리예요.

# API 설정값을 정의합니다.
base_url = "http://data4library.kr/api/keywordList"  # API 주소예요.
auth_key = "f6727fccbbc455cac9b14af79ef28e4b3b9d8db898c217c7abb19bfde8b0d8d8"  # data4library.kr에서 발급받은 API 키를 넣으세요.
isbn13 = "9791159921445"  # 테스트용 ISBN(어린왕자 책)입니다. 원하는 ISBN13으로 바꾸세요.
additional_yn = "Y"  # 추가 정보를 포함하려고 Y로 설정했어요.

# API에 보낼 파라미터를 딕셔너리로 만듭니다.
params = {
    "authKey": auth_key,  # 인증 키를 추가해요.
    "isbn13": isbn13,  # 책의 ISBN을 추가해요.
    "additionalYN": additional_yn  # 추가 정보 옵션을 추가해요.
}

try:  # 오류가 나도 프로그램이 멈추지 않게 try-except를 사용해요.
    # API에 요청을 보내고 응답을 받아옵니다.
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # 응답이 성공(HTTP 200)인지 확인해요. 아니면 오류 발생.

    # 응답이 XML인지 확인합니다. (API는 XML로 응답해요.)
    content_type = response.headers.get("content-type", "")
    if "xml" in content_type.lower():
        # XML을 JSON(딕셔너리)로 변환해요.
        data = xmltodict.parse(response.text)
    else:
        # 만약 JSON이면 바로 파싱(이 API는 XML이 기본이지만요).
        data = response.json()

    # 키워드 데이터가 있는지 확인합니다. (응답 구조: data['response']['keywords']['keyword'])
    if 'response' in data and 'items' in data['response'] and 'item' in data['response']['items']:
        keywords = data['response']['items']['item']  # 키워드 리스트를 가져옵니다.
        
        # 키워드가 단일 딕셔너리일 경우 리스트로 변환해요. (API가 키워드 1개만 줄 때)
        if isinstance(keywords, dict):
            keywords = [keywords]
        
        # 키워드 리스트를 DataFrame으로 변환해요. 키(word, weight)가 컬럼이 됩니다.
        df = pd.DataFrame(keywords)
        
        # DataFrame을 출력해요. (컬럼: word, weight 등)
        print("키워드 DataFrame:")
        print(df)

        # DataFrame을 CSV 파일로 저장해요. 'keywords.csv'라는 이름으로 저장됩니다.
        df.to_csv('keywords.csv', index=False, encoding='utf-8-sig')
        print("\nDataFrame이 'keywords.csv' 파일로 저장되었습니다!")

        # 추가 정보(additionalItem) 출력 (선택 사항).
        if 'additionalItem' in data['response']:
            print("\n책 추가 정보:")
            print(data['response']['additionalItem'])
        
        # 추가로, 예쁘게 보기 위해 DataFrame의 첫 몇 줄만 보여줄 수도 있어요.
        print("\nDataFrame 첫 5줄:")
        print(df.head())
    else:
        # 키워드 데이터가 없으면 메시지를 출력해요.
        print("키워드 데이터가 없습니다. 응답:", data)

except requests.exceptions.HTTPError as e:  # HTTP 오류(예: 인증 실패) 잡기.
    print("HTTP 오류:", e)  # 오류 메시지 출력. (API 키나 ISBN 확인하세요!)
except Exception as e:  # 다른 오류 잡기.
    print("오류 발생:", e)  # 일반 오류 메시지 출력.
