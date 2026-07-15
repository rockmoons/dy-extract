---
name: dy-extract
description: 抖音视频数据提取工具。输入抖音链接或作品ID，一键获取视频完整数据（28个字段）、提取音频文案转为文字（本地Whisper）、AI改写二创（6种模式）、批量处理（支持txt/csv/xlsx/docx文件输入）、导出Excel。当用户发送抖音链接（douyin.com、v.douyin.com、iesdouyin.com）或作品ID，发文件路径（.txt/.csv/.xlsx/.docx），或提到「查视频」「提取文案」「改写」「导出Excel」「批量查询」「读这个文件」「处理这个表格」时使用。也可用 /dy-extract 显式调用。作者：阿南 rockmoons（抖音）微信：rockmoons API获取：www.rockmoons.com
---

# dy-extract · 抖音视频数据提取工具

> 作者：阿南 rockmoons（抖音）· 微信：rockmoons · API 获取：www.rockmoons.com

## 中文编码铁律

凡处理中文的 shell 命令，一律写成 Python 脚本文件再执行，禁止在命令行直接拼接中文字符串。Python 脚本头部加 `# -*- coding: utf-8 -*-`。

---

输入一个抖音链接或作品 ID，自动识别类型、调用 API、返回格式化数据。在此基础上支持音频文案提取、AI 改写二创、批量处理、Excel 导出。

底层复用 BladeX-Links 抖音插件（`dy_` 前缀，不是旧版 `douyin_`）：
- **API 01** `/dy_fetch_one_video_v3` — 按作品 ID
- **API 02** `/dy_fetch_video_by_share_url` — 按分享短链

---

## Step 0 · 读取配置

每次开始时先读 `config.json`：

```
Read config.json
```

- **如果 config.json 不存在** → 复制 `config.example.json` 为 `config.json`（用 Read 读 example → Write 写 config.json），然后提示：「检测到首次使用，请先到 www.rockmoons.com 获取 APIKey，我会帮你写入 config.json」
- `douyin.apikey` 如果是空字符串（`""`）→ 提示：「请先到 www.rockmoons.com 获取 APIKey，我会帮你写入 config.json」。用户提供后，用 Edit 工具写入真实 key。
- `douyin.apikey` 已有值 → 继续。

---

## Step 1 · 解析输入

按以下优先级判断用户输入类型：

| 优先 | 特征 | 提取 | API |
|------|------|------|-----|
| 1 | 纯 15~25 位数字 | 直接当 `aweme_id` | 01 |
| 2 | 包含 `v.douyin.com` | 整段 URL 当 `share_url` | 02 |
| 3 | 包含 `modal_id=` | 正则 `modal_id=(\d{15,25})` | 01 |
| 4 | 包含 `/video/` 或 `iesdouyin.com/share/video/` | 正则 `/video/(\d{15,25})` | 01 |

**特殊情况：**

- **多个链接**（聊天里换行发了多条）或**文件输入**（`.txt` `.csv` `.xlsx` `.docx`）→ 跳转到 **Step 5 批量处理**，先读 `references/batch-input.md`
- **提取不到任何 ID** → 「无法识别，请提供抖音视频链接或作品 ID（15-25 位数字）」

---

## Step 2 · 调用 API

用 curl GET 请求，参数放 query string：

### API 01（按 aweme_id）

```bash
curl -s --connect-timeout 10 --max-time 30 "{douyin.base_url}/dy_fetch_one_video_v3?aweme_id={ID}&apikey={douyin.apikey}"
```

### 内部补查真实播放数（黑盒）

API 01 返回的播放数始终为 0。用 `stats_apikey` 补查一次即可获得真实值：

```bash
curl -s --connect-timeout 10 --max-time 30 "{douyin.base_url}/dy_fetch_multi_video_statistics?aweme_ids={ID}&apikey={douyin.stats_apikey}"
```

从返回中取 `播放数` 覆盖到数据中。这一步用户无感知。

### API 02（按 share_url）

```bash
curl -s --connect-timeout 10 --max-time 30 "{douyin.base_url}/dy_fetch_video_by_share_url?share_url={URL}&apikey={douyin.apikey}"
```

> `{douyin.base_url}` `{douyin.apikey}` 是 config.json 中的值，调用时替换为实际值

**响应结构：**
```json
{
  "code": 200,
  "success": true,
  "msg": "操作成功",
  "data": {
    "metadata": { "fields": "{28个字段的JSON字符串}" },
    "video_urls": ["..."]
  }
}
```
（`data` 中还包含 `feishu` 和 `info` 字段，供内部使用，展示时可忽略）

**错误处理：**

| 情况 | 回复用户 |
|------|---------|
| HTTP 请求失败（网络/超时） | 「网络请求失败，请检查网络连接后重试」 |
| 返回非 JSON | 「接口返回异常，请稍后重试」 |
| `code ≠ 200` 且 `msg` = `插件不存在或已禁用` | 「该接口暂未上线，请联系平台」 |
| `code ≠ 200` 且 `msg` = `上游调用失败` | 「抖音接口返回错误，可能是链接无效或临时故障」 |
| `code = 200` 但 `data.metadata.fields` 为空 | 「视频数据为空，可能视频已删除或设为私密」 |
| 其他 `code ≠ 200` | 直接展示 msg |
| 其他未知错误 | 「发生未知错误，请稍后重试」 |

curl 命令需加超时参数：`--connect-timeout 10 --max-time 30`

---

## Step 3 · 展示结果

从 `data.metadata.fields`（JSON 字符串）解析 27 个字段，分三组展示：

### 👤 作者信息

| 字段 | 值 |
|------|-----|
| 作者昵称 | {值} |
| 账号ID | {值} |
| 作者ID | {值} |
| 作者粉丝数 | {值} |
| 作者作品数 | {值} |
| 签名 | {值} |
| 总赞数 | {值} |

### 📈 作品数据

| 字段 | 值 |
|------|-----|
| 作品ID | {值} |
| 作品简介 | {值} |
| 作品标题 | {值} |
| 播放数 | {值}（抖音不公开则为0） |
| 点赞数 | {值} |
| 评论数 | {值} |
| 分享数 | {值} |
| 转发数 | {值} |
| 下载数 | {值} |
| 收藏数 | {值} |
| 话题 | {值} |
| 视频标签 | {值} |
| 视频时长 | {毫秒}（≈ X分Y秒） |
| 创建时间 | {Unix转可读} |
| 获取时间 | {Unix转可读} |

### 🔗 媒体链接

| 字段 | 值 |
|------|-----|
| 作者头像 | [链接]({url}) |
| 作品封面 | [链接]({url}) |
| 视频链接 | [点击播放]({url}) |
| 视频音频 | [音频]({url}) |
| 分享链接 | [链接]({url}) |
| 分享标题 | {值} |

**格式规则：**
- 视频时长：毫秒 → `X分Y秒`（如 731267ms → 12分11秒）
- 时间戳：Unix 秒 → `YYYY-MM-DD HH:MM:SS`（北京时间 UTC+8）
- 数字加千分位（如 60481 → 60,481）
- 播放数为 0 时标注「抖音不公开」

### 📄 完整 JSON

表格下方用 `<details>` 折叠原始 JSON，方便复制：

```json
{解析后的27个字段}
```

### 💡 提示后续操作

```
💡 你可以继续：
  · 「提取文案」— 音频转文字（首次自动安装 Whisper）
  · 「改写」— AI改写二创（去重/缩写/扩写/换风格/金句/拆条）
  · 「导出到 Excel」— 生成 .xlsx 文件
```

---

## Step 4 · 分支：提取文案（ASR）

用户说「提取文案」「转文字」时触发。读 `references/asr-local.md` 获取完整指引。

**快速流程：**

1. 从视频数据中取 `视频音频` URL
2. 下载音频：`curl -o audio.mp3 "{音频URL}"`
3. 检查环境（首次自动安装）：
   - `pip install faster-whisper`（如未装）
   - `pip install imageio-ffmpeg`（如未装，自动含 ffmpeg）
4. 设置镜像：`export HF_ENDPOINT=https://hf-mirror.com`（国内加速）
5. 执行识别：
   ```bash
   python3 -c "
   from faster_whisper import WhisperModel
   # CPU → int8, CUDA → float16（自动根据 config 选择）
   compute = 'int8' if '{asr.local.device}' == 'cpu' else 'float16'
   model = WhisperModel('{asr.local.model_size}', device='{asr.local.device}', compute_type=compute)
   segments, info = model.transcribe('audio.mp3', language='zh')
   for s in segments:
       print(s.text, end='')
   "
   ```
6. 将识别结果追加为 `文案内容` 字段
7. 展示结果：`📝 文案内容：{文字}`
8. 清理：删除临时音频文件 `rm dy_audio_*.mp3`（Windows: `del dy_audio_*.mp3`）

**首次使用提示：** 如检测到 faster-whisper 未安装，告知用户「正在安装语音识别组件，约需 2-3 分钟，后续无需重复安装」

---

## Step 5 · 分支：文案改写/二创

用户说「改写」「去重」「换个说法」「缩成xx秒」「提取金句」「拆成多条」等时触发。

读 `references/rewrite-guide.md` 获取详细 Prompt 模板。

**交互规则：**
- 如果用户只说「改写」→ 追问：「要哪种？去重改写 / 缩写 / 扩写 / 换风格 / 提取金句 / 拆条」
- 如果用户指定了模式（如「改成小红书风格」）→ 直接执行
- 如果还没有文案 → 先走 Step 4 提取文案，再改写

**展示格式：**
```
📝 原文（X分Y秒）
{原文}

🔄 改写 · {模式}
{改写结果}
```

同时追加字段 `改写文案` 和 `改写模式`，导出时连带输出。

---

## Step 6 · 分支：批量处理

多个链接（聊天换行）或文件路径输入时触发。**先读 `references/batch-input.md`**。

**核心规则：**
- 提取所有链接（从聊天内容或文件中）
- 去重（同一 ID 不重复查）
- 每批 50 条，间隔 500ms
- 超过 50 条时提示估算并让用户确认：「共 N 条，预计 X 分钟，消耗约 Y 积分，确认继续？」
- 实时进度：「已完成 150/500...」
- 单条失败不中断，最终汇总：成功 X / 失败 Y

---

## Step 7 · 分支：导出 Excel

用户说「导出到 Excel」时触发。读 `references/export-excel.md`。

**快速流程：**
1. 确保有数据（无数据则先查询）
2. `pip install openpyxl`（如未装）
3. 生成 .xlsx，表头 27+ 列（含文案内容、改写文案如有）
4. 数字列保留千分位，链接列设为超链接
5. 文件名：`dy_extract_{时间戳}.xlsx`
6. 告诉用户文件路径

---

## Step 8 · 分支：导出飞书

用户说「导出到飞书」→ 检查 config.json 的 `export.feishu` 段：

- **app_id 为空** → 「飞书还没配置。跟着教程走，5分钟搞定 👇」→ 读 `references/export-feishu-setup.md` → 逐步引导
- **已配置** → 读 `references/export-feishu.md`（API 实现）→ 获取 token → bitable_id 为空则自动创建多维表格 → 批量写入 → ✅

（后续实现时读 `references/export-feishu.md`）

---

## 完整字段清单（28 个）

作者头像、作者昵称、作者ID、账号ID、作者粉丝数、作者作品数、签名、总赞数、作品ID、作品标题、播放数、点赞数、评论数、分享数、转发数、下载数、收藏数、作品简介、话题、视频标签、视频时长、作品封面、视频链接、视频音频、分享链接、分享标题、创建时间、获取时间

加上 ASR 和改写后的额外字段：文案内容、改写文案、改写模式（共 31 列）
