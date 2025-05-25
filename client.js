//モジュールのインポート
const net = require("net");
const fs = require("fs");

// ソケットパスの定義
const socketPath = "/tmp/socket_file";

//リクエストデータ(jsオブジェクト)
const request = {
  method: "subtract",
  params: [42, 23],
  param_types: ["int", "int"],
  id: 1
};

//サーバへの接続と通信
const client = net.createConnection(socketPath, () => {
  console.log("Connected to RPC server");
  client.write(JSON.stringify(request)); //jsonに変換して送信
  console.log("Waiting for results...");
});

// サーバからのデータ受信イベント
//"data":「データ受信イベント」、(data) :「受信したデータそのもの」
client.on("data", (data) => {
  // 受信したデータはBufferなので文字列に変換してJSONパース（json形式の文字列をjsのオブジェクトに変換する）
  const response = JSON.parse(data.toString());
  console.log("Received response from server:", response);

  // 通信終了
  client.end();
});
