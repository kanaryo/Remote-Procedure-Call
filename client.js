//モジュールのインポート
const net = require("net");
const fs = require("fs");

// ソケットパスの定義
const socketPath = "/tmp/socket_file";

//リクエストデータ(jsオブジェクト)
const requests = [
  {
    method: "subtract",
    params: [42, 23],
    param_types: ["int", "int"],
    id: 1
  },
  {
    method: "floor",
    params: [4.7],
    param_types: ["float"],
    id: 2
  },
  {
    method: "nroot",
    params: [2, 16],
    param_types: ["int", "int"],
    id: 3
  },
  {
    method: "reverse",
    params: ["hello"],
    param_types: ["string"],
    id: 4
  },
  {
    method: "validAnagram",
    params: ["listen", "silent"],
    param_types: ["string", "string"],
    id: 5
  },
  {
    method: "sort",
    params: [["banana", "apple", "cherry"]],
    param_types: ["string[]"],
    id: 6
  }
];

//サーバへの接続と通信
const client = net.createConnection(socketPath, () => {
  console.log("Connected to RPC server");

  for (const req of requests) {
    client.write(JSON.stringify(req) + '\n'); // JSON文字列に変換して送信
  }  
  
  console.log("Waiting for results...");
});

// サーバからのデータ受信イベント
//"data":「データ受信イベント」、(data) :「受信したデータそのもの」
let buffer = "";

client.on('data', (data) => {
  buffer += data.toString();

  let boundary = buffer.indexOf('\n');
  while (boundary !== -1) {
    const jsonStr = buffer.substring(0, boundary);
    buffer = buffer.substring(boundary + 1);

    try {
      const response = JSON.parse(jsonStr);
      console.log("Received response from server:", response);
    } catch (e) {
      console.error("Failed to parse JSON:", e);
    }

    boundary = buffer.indexOf('\n');
  }
});

client.on("end", () => {
  console.log("Disconnected from server");
});