import socket
import os
import json
import math

# サーバで提供する関数
def subtract(a, b):
    return a - b

def floor(x):
    return math.floor(x)  # xを切り捨てて整数に

def nroot(n, x):
    if n == 0:
        raise ValueError("n cannot be zero")
    return x ** (1 / n)

def reverse(s):
    return s[::-1]

def validAnagram(str1, str2):
    return sorted(str1) == sorted(str2)

def sort(strArr):
    if not isinstance(strArr, list):
        raise ValueError("Input must be a list of strings")
    return sorted(strArr)

# 利用可能な関数を辞書（ハッシュマップ）で管理
METHODS = {
    "subtract": subtract,
    "floor": floor,
    "nroot": nroot,
    "reverse": reverse,
    "validAnagram": validAnagram,
    "sort": sort
}

#ソケットの作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

#UNIXソケットのパスを設定
server_address = '/tmp/socket_file'

# 以前の接続が残っていた場合にサーバアドレスを削除
try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

#サーバアドレスにソケットをバインド（接続）
sock.bind(server_address)

sock.listen(1)

while True:
    print("Waiting for a connection...")

    connection, client_address = sock.accept()
    try:
        print('Connection established from', client_address)
        buffer = ""  # 受信データをためるバッファ

        while True:
            data = connection.recv(1024)
            if not data:
                print("No more data from client.")
                break

            buffer += data.decode('utf-8')

            # 改行で複数リクエストを分割処理
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if not line.strip():
                    continue

                print("Received data:", line)

                try:
                    request = json.loads(line)
                    method = request.get("method")
                    params = request.get("params", [])
                    request_id = request.get("id")

                    if method in METHODS:
                        result = METHODS[method](*params)
                        print("Calculation result:", result)
                        response = {
                            "result": result,
                            "error": None,
                            "id": request_id
                        }
                    else:
                        response = {
                            "result": None,
                            "error": f"Method '{method}' not found",
                            "id": request_id
                        }
                except Exception as e:
                    response = {
                        "result": None,
                        "error": str(e),
                        "id": None
                    }

                response_json = json.dumps(response) + '\n'  # 忘れずに改行つけて返す
                connection.sendall(response_json.encode('utf-8'))

    finally:
        print("Closing current connection")
        connection.close()