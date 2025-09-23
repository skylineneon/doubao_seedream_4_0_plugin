# 豆包 Seedream 4.0 - Dify 插件

基于火山引擎方舟 Doubao Seedream 4.0 的 AI 文生图插件。提供同步的文本生成图像工具，返回 PNG 字节给工作流使用。

## 功能特性

- 使用 Doubao Seedream 4.0（`doubao-seedream-4-0-250828`）进行文生图
- 可配置输出尺寸（如 `2048x2048`、`2560x1440`）


## 环境要求

- Python 3.12（参见 `manifest.yaml`）
- 依赖（见 `requirements.txt`）：
  - `dify_plugin>=0.1.0,<0.2.0`
  - `openai>=1.13.0`
  - `requests>=2.31.0`
  - `Pillow>=10.0.0`
  - `tiktoken>=0.7.0`

## 安装

1) 创建并激活 Python 3.12 环境。
2) 安装依赖：

```
pip install -r requirements.txt
```

3) 确保网络可访问火山引擎方舟相关端点。

## 运行

- 本地开发运行：

```
python main.py
```

运行时设置 `MAX_REQUEST_TIMEOUT=600` 秒，以适应图像生成时长。

## 凭据配置

本插件需要 Doubao API Key：

- 从方舟控制台获取：`https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey`
- 通过插件凭据 UI（定义于 `provider/doubao_provider.yaml`）配置为 `api_key`。

## 工具：text2image

- 端点：`POST https://ark.cn-beijing.volces.com/api/v3/images/generations`
- 模型：`doubao-seedream-4-0-250828`
- 请求字段（部分）：
  - `prompt`（字符串，必填）
  - `size`（字符串，选填；默认 `2048x2048`）
  - `response_format`：`url`
  - `sequential_image_generation`：`auto`
  - `stream`：`false`
  - `watermark`：`false`

- 响应处理：
  - 校验 HTTP 状态
  - 解析 JSON，读取 `data[*].url`
  - 逐个下载并在内存中转为 PNG，返回字节

## 错误处理与日志

- 对缺失凭据与参数进行防御性检查
- 提供清晰的进度与错误提示
- 最小化日志内容，不含敏感信息（不记录提示词/API Key）

## 隐私

详见 `PRIVACY.md` 与 `PRIVACY.zh-Hans.md`。摘要：提示词通过 HTTPS 发送至 Ark，图像以 PNG 字节返回；插件不做持久化存储。

## 开发说明

- 提供方包含本地凭据格式校验；连通性校验默认注释
- 为长时生成配置了超时与日志

## 许可

本仓库可能包含依赖各自许可的素材。许可详情请联系项目所有者。
