import requests
import time
import json
from PIL import Image
from io import BytesIO

base_url = "https://api-inference.modelscope.cn/"
api_key = "ms-3b684a6c-63f3-4764-b929-c79f5e888df2"

common_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# 添加调试信息
print(f"使用API密钥: {api_key[:10]}...")
print(f"请求URL: {base_url}v1/images/generations")

try:
    response = requests.post(
        f"{base_url}v1/images/generations",
        headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
        data=json.dumps(
            {
                "model": "black-forest-labs/FLUX.1-Krea-dev",  # ModelScope Model-Id, required
                "prompt": "a cute cat",
            },
            ensure_ascii=False,
        ).encode("utf-8"),
    )

    print(f"响应状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")

    if response.status_code == 401:
        print("错误: 401 未授权")
        print("可能的原因:")
        print("1. API密钥无效或已过期")
        print("2. API密钥格式不正确")
        print("3. 账户权限不足")
        print(f"响应内容: {response.text}")
        exit(1)

    response.raise_for_status()
    task_id = response.json()["task_id"]
    print(f"任务ID: {task_id}")

    while True:
        result = requests.get(
            f"{base_url}v1/tasks/{task_id}",
            headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
        )
        result.raise_for_status()
        data = result.json()

        if data["task_status"] == "SUCCEED":
            image = Image.open(BytesIO(requests.get(data["output_images"][0]).content))
            image.save("result_image.jpg")
            print("图片生成成功！已保存为 result_image.jpg")
            break
        elif data["task_status"] == "FAILED":
            print("图片生成失败")
            print(f"错误信息: {data}")
            break
        else:
            print(f"任务状态: {data['task_status']}")

        time.sleep(5)

except requests.exceptions.HTTPError as e:
    print(f"HTTP错误: {e}")
    if hasattr(e, "response") and e.response is not None:
        print(f"响应内容: {e.response.text}")
except requests.exceptions.RequestException as e:
    print(f"请求错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
