# 飞书多维表格 API 实现

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
curl -s -X POST https://open.feishu.cn/open-apis/bitable/v1/apps \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name":"抖音视频数据"}'
```

返回 `{ "app": { "app_token": "..." } }` → 存为 `bitable_id`。

然后创建表：

```bash
curl -s -X POST https://open.feishu.cn/open-apis/bitable/v1/apps/{bitable_id}/tables \
  -H "Authorization: Bearer {token}" \
  -d '{"table":{"name":"视频列表","fields":[...]}}'
```

fields 按导出字段（28列）自动生成，类型：
- 文本列 → `{ "field_name": "作者昵称", "type": 1 }`
- 数字列 → `{ "field_name": "点赞数", "type": 2 }`

返回 `{ "table_id": "..." }` → 存 config.json。

### 删除默认空字段

飞书新建表格自带 4 个空白字段（文本、单选、日期、附件），需在写入数据后删除：

```bash
# 列出所有字段
curl -s "https://open.feishu.cn/open-apis/bitable/v1/apps/{bitable_id}/tables/{table_id}/fields" \
  -H "Authorization: Bearer {token}"

# 删除前 4 个默认字段（field_name 为 "文本"/"单选"/"日期"/"附件"）
for id in {默认字段id列表}; do
  curl -s -X DELETE "https://open.feishu.cn/open-apis/bitable/v1/apps/{bitable_id}/tables/{table_id}/fields/$id" \
    -H "Authorization: Bearer {token}"
done
```

---

## Step 3 · 批量写入

```bash
curl -s -X POST https://open.feishu.cn/open-apis/bitable/v1/apps/{bitable_id}/tables/{table_id}/records/batch_create \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"records":[{...}]}'
```

每批最多 500 条，超量分批写入。

---

## 完成提示

```
✅ 已导入 N 条到飞书多维表格「抖音视频数据」
   打开飞书 → 云文档 → 就能看到
```
