import socket
import os
import json

# サーバで提供する関数
def subtract(a, b):
    return a - b

# 利用可能な関数を辞書（ハッシュマップ）で管理
METHODS = {
    "subtract": subtract
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
        
        while True:
            #データ取得
            data = connection.recv(1024)
            if not data:
                print("No more data from client.")
                break            
            
            #データを出力してデバッグ
            # if data:
            #     print("Received data:", data.decode('utf-8'))
            # else:
            #     print("No more data from client.")
            #     break   
            
            decoded_data = data.decode('utf-8')
            print("Received data:", decoded_data)
            
            try:
                request = json.loads(decoded_data) #JSON文字列をPythonの辞書（dict）に変換
                method = request.get("method")
                params = request.get("params", [])
                request_id = request.get("id")  

                if method in METHODS:
                    result = METHODS[method](*params) #辞書 METHODS に対してキー method を指定して、その値（関数）を取得。引数にparamsを展開して渡す
                    print("Calculation result:", result)  # ここで結果を出力してデバッグ

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
                
            # レスポンスをクライアントに送信
            response_json = json.dumps(response) #Pythonの辞書（response）をJSON形式の文字列に変換
            connection.sendall(response_json.encode('utf-8')) #JSON文字列をUTF-8エンコードして、バイト列に変換。接続中のクライアントに対して、エンコードしたバイト列（JSONレスポンス）をすべて送信。
            
        else:
            print('no data from', client_address)
            break

    finally:
        print("Closing current connection")
        connection.close()