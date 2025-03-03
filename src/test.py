from websockets.sync.client import connect
import requests as req
import jwt

if __name__ == "__main__":
    access_token: str = ''
    token_req = req.post(
        url='http://127.0.0.1:8000/api/v1/account/login/',
        data={
            'username': 'string',
            'password': 'string'
        }
    )
    if token_req.status_code == 200:
        access_token = token_req.json().get('access_token')
        print(access_token)
    try:
        with connect(uri=f'ws://127.0.0.1:8000/api/ws/5e41bca3-5731-40da-b65d-4c6927e8179b/', additional_headers={"Authorization": f"Bearer {access_token}"}) as ws:
            ws.send("Hello")
            print(ws.recv())
    except Exception as e:
        raise e