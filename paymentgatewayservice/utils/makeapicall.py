import requests

def make_api_call(url, method, headers={}) -> dict[str, str]:
    try:
        response = requests.request(method, url, headers=headers)
        return (
            response.json() if response.status_code == 200 else {"error": response.text}
        )
    except Exception as e:
        return {"error": str(e)}