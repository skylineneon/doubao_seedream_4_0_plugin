# Doubao Seedream 4.0 - Dify Plugin

AI text-to-image generation plugin powered by Doubao Seedream 4.0 on Volcano Engine Ark. Provides a synchronous tool to generate images from text prompts and return PNG bytes to your workflow.

## Features

- Text-to-image via Doubao Seedream 4.0 (`doubao-seedream-4-0-250828`)
- HTTPS calls to Ark Images Generations API: `https://ark.cn-beijing.volces.com/api/v3/images/generations`
- Configurable output sizes (e.g., `2048x2048`, `2560x1440`)
- Synchronous generation flow with progress text messages
- In-memory PNG conversion and direct binary return

## Directory Structure

- `main.py`: Starts the plugin with extended timeout
- `manifest.yaml`: Plugin metadata and runtime definition
- `provider/`: Tool provider definition and credentials validation
  - `doubao_provider.yaml`: UI/metadata and credentials schema
  - `doubao_provider.py`: Provider implementation (credentials checks)
- `tools/`: Tool implementation and schema
  - `text2image.py`: Core text-to-image logic against Ark API
  - `text2image.yaml`: Tool identity and parameters
- `test/`: Example/testing scripts
- `PRIVACY.md` / `PRIVACY.zh-Hans.md`: Privacy policies (EN/ZH)

## Requirements

- Python 3.12 (as defined in `manifest.yaml`)
- Dependencies (see `requirements.txt`):
  - `dify_plugin>=0.1.0,<0.2.0`
  - `openai>=1.13.0`
  - `requests>=2.31.0`
  - `Pillow>=10.0.0`
  - `tiktoken>=0.7.0`

## Installation

1) Create and activate a Python 3.12 environment.
2) Install dependencies:

```
pip install -r requirements.txt
```

3) Ensure your environment can access Volcano Engine Ark network endpoints.

## Run

- Local run (for development):

```
python main.py
```

This starts the plugin runtime with `MAX_REQUEST_TIMEOUT=600` seconds to accommodate image generation.

## Configure Credentials

The plugin requires a Doubao API Key:

- Obtain from Volcano Engine Ark console: `https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey`
- Provide it via the plugin credentials UI (defined in `provider/doubao_provider.yaml`) as `api_key`.

## Tool: text2image

- Endpoint: `POST https://ark.cn-beijing.volces.com/api/v3/images/generations`
- Model: `doubao-seedream-4-0-250828`
- Request fields (subset):
  - `prompt` (string, required)
  - `size` (string, optional; default `2048x2048`)
  - `response_format`: `url`
  - `sequential_image_generation`: `auto`
  - `stream`: `false`
  - `watermark`: `false`

- Response handling:
  - Validates HTTP status
  - Parses JSON; expects `data[*].url`
  - Downloads each URL, converts to PNG in-memory, returns bytes

## Error Handling & Logging

- Defensive checks for missing credentials and parameters
- Informative progress messages
- Minimal logging without sensitive data (no prompts/API keys)

## Privacy

See `PRIVACY.md` and `PRIVACY.zh-Hans.md` for details. In short: prompts are sent to Ark over HTTPS; images are returned as PNG bytes; no persistent storage by the plugin.

## Development Notes

- Provider includes local credential format checks; connectivity checks are stubbed by default
- Timeout and logging configured for long-running image generations

## License

This repository may include assets under their respective licenses. Consult the project owner for licensing details.
