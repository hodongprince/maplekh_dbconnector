import json
from urllib.parse import urlencode

# JSON 객체
data = {
  "name": "John Doe",
  "age": 30
}

# JSON 객체를 문자열로 변환
json_str = json.dumps(data)

# URL 인코딩 적용
encoded_json_str = urlencode({"json": json_str})

# 최종 URL
base_url = "https://example.com/api"
final_url = f"{base_url}?{encoded_json_str}"

print(final_url)