# dy-extract · 抖音视频数据提取工具

输入抖音链接，一键获取视频数据、提取文案、改写二创、导出 Excel。

---

## ⚡ 快速开始

1. 确保已安装 ZCode
2. 将 `dy-extract/` 整个文件夹复制到你项目的 `.agents/skills/` 目录下：
   ```
   你的项目/
   └── .agents/
       └── skills/
           └── dy-extract/    ← 放这里
               ├── SKILL.md
               ├── config.json
               ├── README.md
               └── references/
   ```
3. 复制 `config.example.json` 为 `config.json`（如果还没有的话）
4. 打开 `config.json`，将 `douyin.apikey` 改为你自己的 APIKey（从 [www.rockmoons.com](https://www.rockmoons.com) 获取）
5. 在 ZCode 对话中发送抖音链接，或输入 `/dy-extract`

首次使用时如果提示 APIKey 未配置，直接把 key 发给模型即可，它会自动写入。

---

## 🔧 环境要求

| 项目 | 基础功能 | 含文案提取 |
|------|---------|-----------|
| Python | 不需要 | ≥ 3.8 |
| 可用内存 | 不需要 | ≥ 4GB |
| 空闲磁盘 | 不需要 | ≥ 5GB |
| 显卡 | 不需要 | 不需要 |

> 只查视频数据不需要 Python。提取文案时模型会自动安装依赖。

---

## 🎯 功能一览

### 1. 查视频数据

发一个抖音链接，返回 28 个字段的完整数据：作者信息、播放/点赞/评论/收藏/分享、封面、视频链接等。

```
你：https://www.douyin.com/video/7661571300523085094
模型：[三组表格 + JSON]
```

### 2. 提取文案

说「提取文案」，模型自动下载视频音频 → 本地语音识别 → 输出文字。

首次使用会**自动安装** Whisper（约需 2-3 分钟），后续即时可用。

```
你：提取文案
模型：📝 全美第一狙击手临危受命保护总统，到头来却沦为替罪羔羊...
```

### 3. AI 改写二创

拿到文案后说「改写」，AI 直接帮你重写。支持 6 种模式：

| 模式 | 说明 | 怎么说 |
|------|------|--------|
| 去重改写 | 换说法不换意思 | 「改写」「去重」 |
| 缩写 | 浓缩到 30s / 15s | 「缩成 30 秒」 |
| 扩写 | 补充细节、场景 | 「扩写」 |
| 换风格 | 小红书 / 新闻稿 / 幽默风 | 「改成小红书风格」 |
| 提取金句 | 抓最精彩 1-2 句 | 「提取金句」 |
| 拆条 | 一段拆多条 | 「拆成 5 条」 |

### 4. 批量处理

一次发多个链接，或上传 txt / csv / excel / word 文件，全部查完统一导出。

超过 50 条会自动提示估算结果，确认后分批执行。

```
你：读 links.txt，全部查，导出 Excel
模型：共 500 条，预计 8 分钟，消耗 5000 积分，确认继续？
你：确认
模型：[50/500]...[500/500] 成功 498 失败 2 ✅ 已导出
```

### 5. 导出 Excel

查完数据后说「导出到 Excel」，生成 .xlsx 文件，每行一个视频，28+ 列。

```
你：导出到 Excel
模型：✅ dy_extract_20260714_123000.xlsx 已生成
```

---

## 📋 支持的链接格式

| 格式 | 示例 |
|------|------|
| 纯数字 ID | `7661571300523085094` |
| 分享短链 | `https://v.douyin.com/xxxxx/` |
| modal_id 链接 | `https://www.douyin.com/jingxuan?modal_id=xxx` |
| 视频直链 | `https://www.douyin.com/video/xxx` |
| iesdouyin 链接 | `https://www.iesdouyin.com/share/video/xxx/` |

---

## ⚙️ config.json 说明

```json
{
  "douyin": {
    "apikey": "你的APIKey",           // 从 www.rockmoons.com 获取
    "base_url": "..."                 // 不用改
  },
  "asr": {
    "provider": "local",              // local=本地识别, cloud=云端(暂未开放)
    "local": {
      "model_size": "medium",         // tiny/small/medium/large, 越大越准越慢
      "language": "zh",
      "device": "cpu"                 // cpu 或 cuda（有 NVIDIA 显卡可改）
    }
  },
  "export": {
    "feishu": { ... }                 // 飞书导出（暂未开放）
  },
  "batch": {
    "chunk_size": 50,                 // 每批处理条数
    "interval_ms": 500                // 批次间隔（毫秒）
  }
}
```

---

## 🔌 获取 APIKey

访问 [www.rockmoons.com](https://www.rockmoons.com) 注册获取 BladeX-Links 平台 APIKey。

注册后可调用 11 个抖音数据接口（视频详情、用户信息、搜索、评论等）。

---

## 📞 联系作者

| 项目 | 内容 |
|------|------|
| 作者 | 阿南 rockmoons（抖音） |
| 微信 | rockmoons |
| 官网 | [www.rockmoons.com](https://www.rockmoons.com) |

---

## 🚧 即将上线

- 云端语音识别（比本地更快）
- 飞书多级表格导出
- 更多改写模板
