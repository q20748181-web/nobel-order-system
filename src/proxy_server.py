#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nobel订单管理系统 - 反向代理服务
将外部访问转发到 Streamlit 应用
"""

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Streamlit 本地地址
STREAMLIT_URL = "http://localhost:8501"

@app.get("/")
async def proxy_root():
    """代理根路径"""
    async with httpx.AsyncClient() as client:
        response = await client.get(STREAMLIT_URL)
        return Response(content=response.content, status_code=response.status_code,
                       headers=dict(response.headers))

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy_request(request: Request, path: str):
    """代理所有请求到 Streamlit"""
    url = f"{STREAMLIT_URL}/{path}"

    # 收集请求体
    body = await request.body()

    # 转发请求
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=body,
            follow_redirects=True,
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 启动反向代理服务...")
    uvicorn.run(app, host="0.0.0.0", port=9001)
