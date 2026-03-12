# HuskLLM - OpenAI 风格 FastAPI 服务

一个使用 FastAPI 实现的、符合 OpenAI 大模型常用接口格式的服务骨架。接口的内部处理逻辑留空，返回结构遵循 OpenAI 公共 API 的字段规范，便于后续替换为真实推理或业务逻辑。

## 项目概览
- 技术栈：Python、FastAPI、Uvicorn
- 主要文件：
  - 服务实现：[main.py](./main.py)
  - 单元测试（前四个接口）：[tests/test_first_four.py](./tests/test_first_four.py)
- 目标：快速提供与 OpenAI API 兼容的路由与响应骨架，用作开发、联调或网关接入的替身服务

## 已实现接口
- 模型
  - GET /v1/models
  - GET /v1/models/{model_id}
- 聊天与补全
  - POST /v1/chat/completions
  - POST /v1/completions
- 向量与安全
  - POST /v1/embeddings
  - POST /v1/moderations
- 图片
  - POST /v1/images/generations
  - POST /v1/images/edits
  - POST /v1/images/variations
- 音频
  - POST /v1/audio/transcriptions
  - POST /v1/audio/translations
- 文件
  - GET /v1/files
  - POST /v1/files
  - GET /v1/files/{file_id}
  - DELETE /v1/files/{file_id}
  - GET /v1/files/{file_id}/content
- 微调
  - POST /v1/fine_tuning/jobs
  - GET /v1/fine_tuning/jobs
  - GET /v1/fine_tuning/jobs/{job_id}
  - POST /v1/fine_tuning/jobs/{job_id}/cancel
- Assistants/Threads（路由骨架）
  - POST /v1/assistants, GET /v1/assistants, GET /v1/assistants/{assistant_id}, DELETE /v1/assistants/{assistant_id}
  - POST /v1/threads, GET /v1/threads/{thread_id}
  - POST /v1/threads/{thread_id}/messages, GET /v1/threads/{thread_id}/messages
  - POST /v1/threads/{thread_id}/runs, GET /v1/threads/{thread_id}/runs/{run_id}, POST /v1/threads/{thread_id}/runs/{run_id}/cancel

## 快速开始
1) 创建并启用虚拟环境
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install fastapi uvicorn httpx
```

2) 启动服务
```bash
python main.py
# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3) 简单调用示例
```bash
# 列出模型
curl http://localhost:8000/v1/models

# Chat Completions
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"你好"}]}'

# Embeddings
curl -X POST http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-3-small","input":"hello"}'
```

## 测试
- 本项目提供了针对前四个接口的单元测试，使用 unittest + fastapi.testclient
- 运行测试：
```bash
. .venv/bin/activate
python -m unittest -v tests/test_first_four.py
```

## 目录结构
```text
EchoLM/                    # 物理目录（重命名后将变为 HuskLLM/）
├─ main.py                 # FastAPI 应用与全部路由骨架
├─ tests/
│  └─ test_first_four.py   # 前四个接口的单元测试
└─ README.md               # 项目说明
```

## 开发说明
- 请求处理逻辑均留空，仅返回符合 OpenAI 接口格式的占位数据
- 可按需在对应路由中接入实际模型推理、存储或鉴权逻辑
- 若新增接口，请遵循现有字段命名与对象结构，保持兼容性

## 目录重命名
- 在项目上级目录执行以下命令完成物理重命名：
```bash
cd /path/to/Workspace/51_OpenClaw
mv EchoLM HuskLLM
```

## 后续扩展建议
- 补充流式响应（SSE）以模拟真实 Chat/Completion 的流式输出
- 接入鉴权中间件（如基于 API Key 的校验）
- 增加日志与请求追踪（如 trace id），便于联调与排障
- 丰富测试覆盖率，包含异常分支与边界条件
