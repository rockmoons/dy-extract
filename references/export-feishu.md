# 飞书多级表格导出（预留）

> ⏳ 此功能尚未实现，等待后续开发。

当前用户说「导出到飞书」时，回复：
「飞书导出功能开发中，敬请期待。当前支持导出 Excel。」

---

## 计划实现方案

### 前置条件
- 飞书开放平台创建企业自建应用
- 获取 `app_id` 和 `app_secret`
- 开通 Bitable（多级表格）权限
- 创建或获取目标 Bitable 的 `bitable_id` 和 `table_id`

### API 流程

1. 获取 tenant_access_token：
   ```
   POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
   Body: { "app_id": "...", "app_secret": "..." }
   ```

2. 批量写入记录：
   ```
   POST https://open.feishu.cn/open-apis/bitable/v1/apps/{bitable_id}/tables/{table_id}/records/batch_create
   Header: Authorization: Bearer {token}
   Body: { "records": [...] }
   ```

### 字段映射（27+2 字段 → 飞书字段类型）
- 文本字段 → type: 1
- 数字字段 → type: 2
- 链接字段 → type: 1（存 URL 文本）

### config.json 配置
```json
"export": {
  "feishu": {
    "app_id": "",
    "app_secret": "",
    "bitable_id": "",
    "table_id": ""
  }
}
```

---

## 待办
- [ ] 实现飞书 OAuth / tenant token 获取
- [ ] 实现 Bitable 批量写入
- [ ] 字段自动创建（首次写入时检测缺失字段）
- [ ] 追加模式 vs 覆盖模式选择
