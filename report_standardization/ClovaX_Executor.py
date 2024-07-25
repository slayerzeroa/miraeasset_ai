import requests
import json

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        full_response = ""
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data:"):
                        json_data = decoded_line[5:].strip()  # 'data:' 이후의 내용 추출 및 공백 제거
                        try:
                            response_json = json.loads(json_data)
                            if "message" in response_json and "content" in response_json["message"] and response_json["outputLength"] != 1:
                                full_response += response_json["message"]["content"]
                        except json.JSONDecodeError:
                            print("Error: Failed to decode JSON")
        self.full_response = full_response
        # 최종 응답 출력