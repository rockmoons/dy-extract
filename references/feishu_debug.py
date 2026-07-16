# -*- coding: utf-8 -*-
"""
飞书多维表格权限诊断脚本
运行方式: 
  1. 在下方填入你的 APP_ID 和 APP_SECRET
  2. python feishu_debug.py
"""
import requests, json, sys

# ===== 请填写你的飞书应用配置 =====
APP_ID = ""       # ← 填你的 App ID
APP_SECRET = ""   # ← 填你的 App Secret
# ==================================

if not APP_ID or not APP_SECRET:
    print("请先在本文件顶部填写 APP_ID 和 APP_SECRET")
    sys.exit(1)

# ... 诊断逻辑保持不变 ...
print("诊断逻辑同上文")
