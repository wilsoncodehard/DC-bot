const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post("/register", (req, res) => {
  const { student_id, name } = req.body;

  // 處理註冊邏輯
  // 假設註冊成功
  console.log(`Received registration: ${student_id}, ${name}`);

  // 這裡可以添加將數據存儲到數據庫或其他後端處理邏輯

  res.json({ message: "Registration successful" });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
