# 필요한 라이브러리를 불러옵니다. requests는 웹 사이트에 요청을 보내는 도구, xmltodict는 XML을 JSON으로 바꾸는 도구예요.
import requests
import xmltodict

# API의 기본 URL을 설정합니다. 이게 도서 키워드 목록을 가져오는 주소예요.
base_url = "http://data4library.kr/api/keywordList"

# 당신의 API 키를 여기에 넣으세요. data4library.kr에서 발급받은 키예요. (비밀키처럼 안전하게 관리하세요!)
auth_key = "f6727fccbbc455cac9b14af79ef28e4b3b9d8db898c217c7abb19bfde8b0d8d8"  # 예: "aaaa1111-bbbb2222-cccc3333-dddd4444"

# 검색할 책의 ISBN13(13자리 숫자)을 여기에 넣으세요. 예시: 어린왕자의 ISBN.
isbn13 = "9791159921445"

# 추가 정보를 포함할지 여부를 설정합니다. 'Y'로 하면 더 많은 키워드 정보를 줘요.
additional_yn = "Y"

# API에 보낼 매개변수(파라미터)를 딕셔너리 형태로 만듭니다. 이게 URL에 붙어서 서버로 전달돼요.
params = {
    "authKey": auth_key,      # API 키를 매개변수에 추가.
    "isbn13": isbn13,         # ISBN을 매개변수에 추가.
    "additionalYN": additional_yn  # 추가 옵션을 매개변수에 추가.
}

# 서버에 GET 요청을 보냅니다. (웹 브라우저가 주소창에 입력하는 것처럼요.) response에 결과를 저장해요.
response = requests.get(base_url, params=params)

# 요청이 성공했는지 확인합니다. (HTTP 상태 코드가 200이 아니면 오류를 발생시켜요.)
response.raise_for_status()

# 서버 응답이 XML 형식인지 확인합니다. (헤더에서 콘텐츠 타입을 봐요.)
content_type = response.headers.get("content-type", "")
if "xml" in content_type.lower():
    # XML 형식이면, xmltodict로 JSON 딕셔너리로 변환합니다. (XML 태그를 키로 바꿔줘요.)
    data = xmltodict.parse(response.text)
else:
    # 만약 JSON이라면 바로 파싱합니다. (하지만 이 API는 XML이에요.)
    data = response.json()

# 변환된 데이터를 출력합니다. print로 화면에 보여줘요. (JSON처럼 보이게 하려면 import json 후 json.dumps(data, ensure_ascii=False, indent=4).print() 해도 좋아요.)
print(data)

# 오류가 발생하면 잡아서 알려줍니다. (try-except는 코드가 중간에 멈추지 않게 해줘요.)
# 이 부분은 코드의 끝에 있지만, 전체를 try 블록으로 감싸는 게 좋아요. (간단히 예시로 추가.)