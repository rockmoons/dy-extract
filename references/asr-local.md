# 本地 Whisper 语音识别 · 全自动安装 & 使用

触发：用户说「提取文案」「转文字」「语音识别」

---

## Step 1 · 获取音频

从视频数据中取 `视频音频` URL（mp3 格式），下载到本地：

```bash
# 跨平台临时文件路径
# Linux/Mac: /tmp/dy_audio_{aweme_id}.mp3
# Windows Git Bash: /tmp/dy_audio_{aweme_id}.mp3
# Windows CMD/PowerShell: 当前目录 dy_audio_{aweme_id}.mp3
# 优先使用当前目录，避免权限问题
curl -o dy_audio_{aweme_id}.mp3 "{音频URL}"
```

---

## Step 2 · 检查 & 自动安装环境

### 2.1 检查 Python
```bash
python3 --version || python --version
```
没有 Python 3.8+ → 提示用户安装：[python.org](https://www.python.org/downloads/)

### 2.2 安装 faster-whisper
```bash
pip show faster-whisper > /dev/null 2>&1 || pip install faster-whisper
```
首次安装约 1 分钟，下载约 200MB。

### 2.3 安装 ffmpeg（自动，无需系统权限）
```bash
pip show imageio-ffmpeg > /dev/null 2>&1 || pip install imageio-ffmpeg
```
`imageio-ffmpeg` 会自动下载一个独立的 ffmpeg 二进制文件，不碰系统环境变量。

### 2.4 设置 Hugging Face 国内镜像（加速模型下载）
```bash
export HF_ENDPOINT=https://hf-mirror.com
```
Windows（CMD）:
```cmd
set HF_ENDPOINT=https://hf-mirror.com
```
Windows（PowerShell）:
```powershell
$env:HF_ENDPOINT="https://hf-mirror.com"
```

---

## Step 3 · 执行语音识别

```bash
python3 -c "
from faster_whisper import WhisperModel
import json

# 根据 config.json 中 asr.local.device 选择 compute_type
# cpu → int8, cuda → float16
compute = 'int8' if '{asr.local.device}' == 'cpu' else 'float16'
model = WhisperModel('{asr.local.model_size}', device='{asr.local.device}', compute_type=compute)
segments, info = model.transcribe('{音频文件路径}', language='{asr.local.language}')

text = ' '.join([s.text for s in segments])
print(text)
"
```

**模型首次下载：** 第一次运行时自动从 Hugging Face 下载模型文件（medium ~1.5GB）。国内镜像 `hf-mirror.com` 加速后通常 1-3 分钟完成。如果下载失败，提示用户检查网络，或换用 `small` 模型。

---

## Step 4 · 返回结果

### 成功
将识别文本返回给用户：

```
📝 文案内容（{X分Y秒}）
{识别文本}
```

同时将此文本追加到视频数据中，作为 `文案内容` 字段。

### 识别为空
```
⚠️ 未能识别到语音内容，可能原因：
  · 视频没有旁白/语音（纯画面或背景音乐）
  · 语音为方言或外语（当前仅支持中文）
```

### 常见错误处理

| 错误 | 处理 |
|------|------|
| `pip: command not found` | 提示安装 Python |
| 模型下载超时 | 检查镜像是否生效，尝试 `export HF_ENDPOINT=https://hf-mirror.com` |
| 内存不足 | 换成 `small` 或 `tiny` 模型 |
| ffmpeg 报错 | 重新 `pip install imageio-ffmpeg` |
| CPU 太慢（>10分钟的音频） | 建议等待，或告知用户后续会支持云端 ASR |

---

## 速度参考（medium 模型，CPU）

| 音频时长 | 约需时间 |
|----------|---------|
| 30 秒 | ~20 秒 |
| 1 分钟 | ~40 秒 |
| 5 分钟 | ~3 分钟 |
| 10 分钟 | ~6 分钟 |
| 30 分钟 | ~20 分钟 |

---

## 清理

识别完成后删除临时音频文件，释放磁盘。
