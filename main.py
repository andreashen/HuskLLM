from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, Response
import logging
import time
import uuid
import base64
import json
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("huskllm")


@app.exception_handler(Exception)
async def _exc_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": {"message": "internal error"}})


def ts():
    return int(time.time())


def rid(prefix: str):
    return f"{prefix}-{uuid.uuid4().hex[:24]}"


def print_req(req: dict):
    data_str = json.dumps(req, ensure_ascii=False)
    logger.info(f"request={data_str}")
    # 同时写入到json文件，文件名带时间戳
    os.makedirs("logs", exist_ok=True)
    curr_ts = ts()
    filename = f"logs/request_{curr_ts}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(req, f, ensure_ascii=False, indent=2)
    if "messages" in req and len(req["messages"]) > 0 and req["messages"][0]["role"] == "system":
        # 提取messages中的content字段
        content = req["messages"][0]["content"]
        # 写入到json文件，文件名带时间戳
        filename = f"logs/system_msg_{curr_ts}.md"
        with open(filename, "w", encoding="utf-8") as f:
            print(content, file=f)


@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "gpt-4o-mini",
                "object": "model",
                "created": ts(),
                "owned_by": "openai",
                "permission": [],
                "root": "gpt-4o-mini",
                "parent": None,
            }
        ],
    }


@app.get("/v1/models/{model_id}")
def retrieve_model(model_id: str):
    return {
        "id": model_id,
        "object": "model",
        "created": ts(),
        "owned_by": "openai",
        "permission": [],
        "root": model_id,
        "parent": None,
    }


@app.post("/v1/chat/completions")
def chat_completions(payload: dict):
    print_req(payload)
    mid = rid("chatcmpl")
    model = payload.get("model", "gpt-4o-mini")
    return {
        "id": mid,
        "object": "chat.completion",
        "created": ts(),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": ""},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


@app.post("/v1/completions")
def text_completions(payload: dict):
    print_req(payload)
    cid = rid("cmpl")
    model = payload.get("model", "gpt-4o-mini")
    return {
        "id": cid,
        "object": "text_completion",
        "created": ts(),
        "model": model,
        "choices": [{"index": 0, "text": "", "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }

# @app.post("/v1/embeddings")
# def embeddings(payload: dict):
#     model = payload.get("model", "text-embedding-3-small")
#     return {
#         "object": "list",
#         "data": [
#             {"object": "embedding", "embedding": [0.0] * 10, "index": 0},
#         ],
#         "model": model,
#         "usage": {"prompt_tokens": 0, "total_tokens": 0},
#     }

# @app.post("/v1/images/generations")
# def images_generations(payload: dict):
#     return {"created": ts(), "data": [{"b64_json": base64.b64encode(b"").decode()}]}

# @app.post("/v1/images/edits")
# async def images_edits(
#     image: UploadFile = File(...),
#     prompt: str = Form(None),
#     mask: UploadFile | None = File(None),
#     model: str = Form("gpt-image-1"),
# ):
#     return {"created": ts(), "data": [{"b64_json": base64.b64encode(b"").decode()}]}

# @app.post("/v1/images/variations")
# async def images_variations(
#     image: UploadFile = File(...), n: int = Form(1), model: str = Form("gpt-image-1")
# ):
#     return {"created": ts(), "data": [{"b64_json": base64.b64encode(b"").decode()}]}

# @app.post("/v1/audio/transcriptions")
# async def audio_transcriptions(
#     file: UploadFile = File(...), model: str = Form("gpt-4o-transcribe")
# ):
#     return {"text": ""}

# @app.post("/v1/audio/translations")
# async def audio_translations(
#     file: UploadFile = File(...), model: str = Form("gpt-4o-transcribe")
# ):
#     return {"text": ""}

# @app.post("/v1/moderations")
# def moderations(payload: dict):
#     mid = rid("modr")
#     model = payload.get("model", "omni-moderation-latest")
#     categories = {
#         "harassment": False,
#         "harassment/threatening": False,
#         "hate": False,
#         "hate/threatening": False,
#         "self-harm": False,
#         "sexual": False,
#         "sexual/minors": False,
#         "violence": False,
#         "violence/graphic": False,
#     }
#     scores = {k: 0.0 for k in categories.keys()}
#     return {
#         "id": mid,
#         "model": model,
#         "results": [{"categories": categories, "category_scores": scores, "flagged": False}],
#     }

# @app.get("/v1/files")
# def list_files():
#     return {
#         "object": "list",
#         "data": [
#             {
#                 "id": rid("file"),
#                 "object": "file",
#                 "bytes": 0,
#                 "created_at": ts(),
#                 "filename": "",
#                 "purpose": "fine-tune",
#             }
#         ],
#     }

# @app.post("/v1/files")
# async def upload_file(file: UploadFile = File(...), purpose: str = Form(None)):
#     return {
#         "id": rid("file"),
#         "object": "file",
#         "bytes": 0,
#         "created_at": ts(),
#         "filename": file.filename,
#         "purpose": purpose or "",
#     }

# @app.get("/v1/files/{file_id}")
# def retrieve_file(file_id: str):
#     return {
#         "id": file_id,
#         "object": "file",
#         "bytes": 0,
#         "created_at": ts(),
#         "filename": "",
#         "purpose": "fine-tune",
#     }

# @app.delete("/v1/files/{file_id}")
# def delete_file(file_id: str):
#     return {"id": file_id, "object": "file", "deleted": True}

# @app.get("/v1/files/{file_id}/content")
# def file_content(file_id: str):
#     return Response(content=b"", media_type="application/octet-stream")

# @app.post("/v1/fine_tuning/jobs")
# def create_fine_tune(payload: dict):
#     jid = rid("ftjob")
#     return {
#         "id": jid,
#         "object": "fine_tuning.job",
#         "created_at": ts(),
#         "finished_at": None,
#         "model": payload.get("model", "gpt-4o-mini"),
#         "fine_tuned_model": None,
#         "organization_id": "org-" + uuid.uuid4().hex[:12],
#         "status": "created",
#         "training_file": payload.get("training_file", ""),
#         "validation_file": payload.get("validation_file"),
#         "result_files": [],
#         "hyperparameters": {"n_epochs": "auto"},
#         "error": None,
#     }

# @app.get("/v1/fine_tuning/jobs")
# def list_fine_tune_jobs():
#     return {"object": "list", "data": []}

# @app.get("/v1/fine_tuning/jobs/{job_id}")
# def retrieve_fine_tune(job_id: str):
#     return {
#         "id": job_id,
#         "object": "fine_tuning.job",
#         "created_at": ts(),
#         "finished_at": None,
#         "model": "gpt-4o-mini",
#         "fine_tuned_model": None,
#         "organization_id": "org-" + uuid.uuid4().hex[:12],
#         "status": "created",
#         "training_file": "",
#         "validation_file": None,
#         "result_files": [],
#         "hyperparameters": {"n_epochs": "auto"},
#         "error": None,
#     }

# @app.post("/v1/fine_tuning/jobs/{job_id}/cancel")
# def cancel_fine_tune(job_id: str):
#     return {"id": job_id, "object": "fine_tuning.job", "status": "cancelled"}

# @app.post("/v1/assistants")
# def create_assistant(payload: dict):
#     aid = rid("asst")
#     return {
#         "id": aid,
#         "object": "assistant",
#         "created_at": ts(),
#         "name": payload.get("name"),
#         "model": payload.get("model", "gpt-4o-mini"),
#         "instructions": payload.get("instructions"),
#         "tools": payload.get("tools", []),
#         "metadata": payload.get("metadata", {}),
#     }

# @app.get("/v1/assistants")
# def list_assistants():
#     return {"object": "list", "data": []}

# @app.get("/v1/assistants/{assistant_id}")
# def retrieve_assistant(assistant_id: str):
#     return {
#         "id": assistant_id,
#         "object": "assistant",
#         "created_at": ts(),
#         "name": "",
#         "model": "gpt-4o-mini",
#         "instructions": "",
#         "tools": [],
#         "metadata": {},
#     }

# @app.delete("/v1/assistants/{assistant_id}")
# def delete_assistant(assistant_id: str):
#     return {"id": assistant_id, "object": "assistant", "deleted": True}

# @app.post("/v1/threads")
# def create_thread(payload: dict):
#     tid = rid("thread")
#     return {"id": tid, "object": "thread", "created_at": ts(), "metadata": payload.get("metadata", {})}

# @app.get("/v1/threads/{thread_id}")
# def retrieve_thread(thread_id: str):
#     return {"id": thread_id, "object": "thread", "created_at": ts(), "metadata": {}}

# @app.post("/v1/threads/{thread_id}/messages")
# def create_message(thread_id: str, payload: dict):
#     mid = rid("msg")
#     return {
#         "id": mid,
#         "object": "thread.message",
#         "created_at": ts(),
#         "thread_id": thread_id,
#         "role": payload.get("role", "user"),
#         "content": payload.get("content", []),
#     }

# @app.get("/v1/threads/{thread_id}/messages")
# def list_messages(thread_id: str):
#     return {"object": "list", "data": []}

# @app.post("/v1/threads/{thread_id}/runs")
# def create_run(thread_id: str, payload: dict):
#     rid_ = rid("run")
#     return {
#         "id": rid_,
#         "object": "thread.run",
#         "created_at": ts(),
#         "thread_id": thread_id,
#         "assistant_id": payload.get("assistant_id"),
#         "status": "queued",
#     }

# @app.get("/v1/threads/{thread_id}/runs/{run_id}")
# def retrieve_run(thread_id: str, run_id: str):
#     return {
#         "id": run_id,
#         "object": "thread.run",
#         "created_at": ts(),
#         "thread_id": thread_id,
#         "assistant_id": None,
#         "status": "queued",
#     }

# @app.post("/v1/threads/{thread_id}/runs/{run_id}/cancel")
# def cancel_run(thread_id: str, run_id: str):
    # return {"id": run_id, "object": "thread.run", "status": "cancelled"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
