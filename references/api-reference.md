# 抖音 API 接口速查表

> 所有路由使用 `dy_` 前缀（非旧版 `douyin_`）
> 基础 URL：`https://api.rockmoons.com/blade-links/openapi/plugin`
> 鉴权：query 参数 `apikey`

---

## 可用接口（8/11）

| # | 路由 | 功能 | 必填参数 | 可选参数 | 状态 |
|---|------|------|---------|---------|------|
| 01 | `/dy_fetch_one_video_v3` | 获取单个视频详情 | `aweme_id` | — | ✅ |
| 02 | `/dy_fetch_video_by_share_url` | 通过分享链接获取视频 | `share_url` | — | ✅ |
| 03 | `/dy_fetch_user_post` | 获取用户发布作品列表 | `sec_user_id` | `max_cursor`, `count` | ✅ |
| 05 | `/dy_fetch_user_profile` | 获取用户主页信息 | `sec_user_id` | — | ✅ |
| 06 | `/dy_fetch_video_comments` | 获取视频评论列表 | `aweme_id` | `cursor`, `count` | ✅ |
| 08 | `/dy_search_videos` | 综合搜索视频 | `keyword` | `offset`, `count`, `sort_type` | ✅ |
| 09 | `/dy_fetch_hot_search` | 实时热搜榜 | — | `board_type` | ✅ |
| 10 | `/dy_fetch_video_statistics` | 获取视频统计数据 | `aweme_ids`（逗号分隔） | — | ✅ |

---

## 未部署接口（3/11）

| # | 路由 | 功能 | 状态 |
|---|------|------|------|
| 04 | `/dy_fetch_user_like` | 获取用户喜欢作品列表 | ❌ |
| 07 | `/dy_fetch_video_comment_replies` | 获取评论的回复列表 | ❌ |
| 11 | `/dy_fetch_user_followings` | 获取用户关注列表 | ❌ |

---

## 通用响应结构

```json
{
  "code": 200,
  "success": true,
  "msg": "操作成功",
  "data": {
    "feishu": {
      "table_fields": "[...]",
      "records": [{ "fields": "{...}" }]
    },
    "video_urls": ["..."],
    "metadata": { "fields": "{...}" },
    "info": "咨询www.rockmoons.com"
  }
}
```

---

## 01 返回的 28 个字段

作者头像、作者昵称、作者ID、账号ID、作者粉丝数、作者作品数、签名、总赞数、作品ID、作品标题、播放数、点赞数、评论数、分享数、转发数、下载数、收藏数、作品简介、话题、视频标签、视频时长、作品封面、视频链接、视频音频、分享链接、分享标题、创建时间、获取时间
