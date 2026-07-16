# 飞书多维表格 API 实现

> **已验证：** 应用通过 `tenant_access_token` 创建的多维表格，自动拥有完整读写权限，无需额外授权。

---

## 前置条件

config.json 已配置 `export.feishu.app_id` 和 `app_secret`（按 `export-feishu-setup.md` 教程完成）。

---

## Step 1 · 获取 token

```bash
curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"{app_id}","app_secret":"{app_secret}"}'
```

返回 `{ "tenant_access_token": "..." }`，缓存 1.5 小时。

---

## Step 2 · 自动创建多维表格（首次）

如果 `bitable_id` 为空，自动创建：

```bash
# 创建多维表格
RESP=$(curl -s -X POST https://open.feishu.cn/open-apis/bitable/v1/apps \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name":"抖音视频数据"}')

# 提取 app_token（即 bitable_id）
BITABLE_ID=$(echo "$RESP" | python -c "import sys,json; print(json.load(sys.stdin)['data']['app']['app_token'])")

# 存到 config.json
```

然后创建表并写入字段（28列全部一起建）：

```bash
# 创建表（一次性定义所有字段）
RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/${BITABLE_ID}/tables" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "table": {
      "name": "视频列表",
      "fields": [
        {"field_name": "作品ID", "type": 1},
        {"field_name": "作品标题", "type": 1},
        {"field_name": "作品简介", "type": 1},
        {"field_name": "作者昵称", "type": 1},
        {"field_name": "作者ID", "type": 1},
        {"field_name": "作者粉丝数", "type": 2},
        {"field_name": "点赞数", "type": 2},
        {"field_name": "评论数", "type": 2},
        {"field_name": "收藏数", "type": 2},
        {"field_name": "分享数", "type": 2},
        {"field_name": "转发数", "type": 2},
        {"field_name": "下载数", "type": 2},
        {"field_name": "播放数", "type": 2},
        {"field_name": "视频时长", "type": 1},
        {"field_name": "发布时间", "type": 1},
        {"field_name": "创建时间", "type": 1},
        {"field_name": "作品封面", "type": 1},
        {"field_name": "视频链接", "type": 1},
        {"field_name": "音频链接", "type": 1},
        {"field_name": "分享链接", "type": 1},
        {"field_name": "分享标题", "type": 1},
        {"field_name": "话题", "type": 1},
        {"field_name": "标签", "type": 1},
        {"field_name": "视频音乐", "type": 1},
        {"field_name": "作者作品数", "type": 2},
        {"field_name": "总赞数", "type": 2},
        {"field_name": "视频合集", "type": 1},
        {"field_name": "作者签名", "type": 1}
      ]
    }
  }')

# 提取 table_id
TABLE_ID=$(echo "$RESP" | python -c "import sys,json; print(json.load(sys.stdin)['data']['table_id'])")

# 存到 config.json
```

> 字段类型：1=文本, 2=数字。建表时一次性定义全部字段，飞书不会自动生成默认字段。

---

## Step 3 · 分享给用户（重要）

应用创建的多维表格保存在**应用的企业云空间**，用户默认看不到。需要把表格链接发给用户：

```bash
# 飞书多维表格链接格式
echo "📋 表格已创建，请点击链接打开：
https://bytedance.feishu.cn/base/${BITABLE_ID}?from=manual"
```

如果知道用户的飞书邮箱或 open_id，也可以直接把用户加为协作者：

```bash
# 把用户加为协作者（可选）
curl -s -X POST "https://open.feishu.cn/open-apis/drive/v1/permissions/${BITABLE_ID}/members?type=bitable&need_notification=false" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "member_type": "email",
    "member_id": "user@example.com",
    "perm": "full_access"
  }'
```

> `member_type` 可选值：`email`（邮箱）、`openid`（用户open_id）、`unionid`（用户union_id）

---

## Step 4 · 批量写入

```bash
# 准备数据（Python 脚本处理中文）
python -c "
import requests, json

token = '{token}'
bitable_id = '{BITABLE_ID}'
table_id = '{TABLE_ID}'

# 一条记录的 fields
records = [
    {'fields': {
        '作品ID': aweme_id,
        '作品标题': title,
        '作品简介': desc,
        # ... 所有字段
    }}
]

# 批量写入（每批最多500条）
url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{bitable_id}/tables/{table_id}/records/batch_create'
resp = requests.post(url,
    headers={'Authorization': f'Bearer {token}'},
    json={'records': records}
)
print(resp.json())
"
```

---

## 完成提示

```
✅ 已导入 N 条到飞书多维表格「抖音视频数据」
   打开飞书 → 云文档 → 就能看到
```
