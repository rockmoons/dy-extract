# 云端 ASR（预留）

> ⏳ 此功能尚未实现，等待用户提供云端 ASR 接口信息。

当前 ASR 使用本地 Whisper（`references/asr-local.md`）。

---

## 待接入

用户将提供云端 ASR 接口，预计信息包括：
- API endpoint URL
- 鉴权方式（APIKey / Token）
- 请求参数格式
- 响应结构
- 支持的音频格式

接入后将更新：
1. 本文件 — 补全 API 调用指引
2. `config.json` — 补全 `asr.cloud` 字段
3. `SKILL.md` — 添加云端 ASR 分支

---

## 当前 config.json 占位
```json
"asr": {
  "cloud": {
    "endpoint": "",
    "apikey": ""
  }
}
```
