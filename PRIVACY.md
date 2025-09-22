# Privacy Policy

This plugin generates images from text using the Doubao Seedream 4.0 model via the Volcano Engine Ark (Doubao) APIs. This document explains how your data is handled when using the plugin.

## Data Processing

- **Text Prompts**: Your text prompts are sent to Volcano Engine Ark (Doubao) Images Generations API to create images.
- **API Communication**: The plugin communicates with Ark endpoints over HTTPS: `https://ark.cn-beijing.volces.com`.
- **Generated Images**: Result images are downloaded from URLs returned by the API, converted to PNG in memory, and streamed back to your workflow.
- **Model Selection**: The tool uses `doubao-seedream-4-0-250828` for image generation. Optional parameters include output size (e.g., `2048x2048`).

## Data Storage

- **No Persistent Storage**: The plugin does not permanently store your prompts or generated images on disk.
- **Temporary Processing**: Images are processed in memory for format conversion and immediately returned. Temporary bytes reside only for the duration of the task.
- **API Key Security**: Your Doubao API key is provided through the plugin credentials system and is not logged or transmitted to any third party other than Ark.

## Third-Party Services

- **Service**: Volcano Engine Ark (Doubao) APIs process your requests according to their terms and privacy policy.
- **Network Communication**: Internet connectivity is required to call Ark endpoints and to download generated image URLs.
- **Model Providers**: Requests are handled by Doubao on Volcano Engine Ark. No OpenAI, Anthropic, Google Gemini, or OpenRouter services are used by this plugin.

## Optional Features

- **Image Size**: You may specify output resolution (e.g., `2048x2048`, `2560x1440`).
- **Streaming**: The tool operates synchronously and returns the generated images and related text messages.

## Data Retention

- The plugin does not retain any user data after completion.
- Generated images are processed in-memory and returned; no persistent copies are kept by the plugin.

## Data Transmission

- Prompts and requests are sent securely over HTTPS to Ark.
- Image URLs are fetched over HTTPS, and images are returned to your workflow as PNG bytes.
- No data is shared with any parties other than Volcano Engine Ark necessary to fulfill the request.

## Credentials & Validation

- The plugin requires a valid Doubao API key configured in credentials.
- The plugin may validate credentials format locally; no validation requests are sent unless explicitly enabled.

## Logging

- Logs record high-level operational messages (e.g., request started/finished, non-sensitive statuses) to aid debugging.
- The plugin avoids logging prompts, API keys, or image content. If errors occur, minimal error context may be logged without sensitive data.