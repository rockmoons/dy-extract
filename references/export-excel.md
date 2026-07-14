# Excel 导出

触发：用户说「导出到 Excel」「导出」「存为 Excel」「生成表格」

---

## 前置检查

```bash
pip show openpyxl > /dev/null 2>&1 || pip install openpyxl
```

---

## 生成 Excel

用 Python openpyxl 库生成 .xlsx 文件。

### 表头（第一行）

按顺序列出所有字段，中文名：

```
作者头像 | 作者昵称 | 作者ID | 账号ID | 作者粉丝数 | 作者作品数 | 签名 | 总赞数 | 作品ID | 作品标题 | 播放数 | 点赞数 | 评论数 | 分享数 | 转发数 | 下载数 | 收藏数 | 作品简介 | 话题 | 视频标签 | 视频时长 | 作品封面 | 视频链接 | 视频音频 | 分享链接 | 分享标题 | 创建时间 | 获取时间 | 文案内容 | 改写文案 | 改写模式
```

其中前 28 列必须有，后 3 列（文案内容、改写文案、改写模式）有数据时才出现。

### 数据行

每行一个视频，从 API 返回的 `metadata.fields` JSON 解析出各字段值填入。

### 格式规则

| 列 | 格式 |
|----|------|
| 数字列（粉丝数、点赞数等） | 数字格式，千分位逗号 |
| 链接列（头像、封面、视频等） | 超链接 HYPERLINK |
| 视频时长 | 毫秒数 + 注释（如 `731267（≈12分11秒）`） |
| 时间戳列 | 转为 `YYYY-MM-DD HH:MM:SS` |
| 文案列 | 纯文本，过长时自动换行 |

### 代码模板

```python
import json
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import datetime

wb = Workbook()
ws = wb.active
ws.title = "抖音视频数据"

# 表头
headers = ["作者头像", "作者昵称", ...]  # 完整 27+ 列
ws.append(headers)

# 数据
for video in videos:
    fields = json.loads(video["metadata"]["fields"])
    row = [fields.get(h, "") for h in headers]
    ws.append(row)

# 保存
filename = f"dy_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
wb.save(filename)
print(filename)
```

---

## 文件名

`dy_extract_{YYYYMMDD}_{HHMMSS}.xlsx`

如 `dy_extract_20260714_123000.xlsx`

生成在当前工作目录下。

---

## 多 Sheet（批量时）

批量 > 1 个视频时，所有视频写入同一个 Sheet。

如果用户明确要求「每个视频一个 Sheet」才拆分。

---

## 完成提示

```
✅ 数据已导出到 dy_extract_20260714_123000.xlsx（{N} 条记录）
```
