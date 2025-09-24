# Doubao Seedream 4.0 - Dify Plugin (Text-to-Image)

AI text-to-image plugin based on Volcano Engine Ark Doubao Seedream 4.0. Supports generating and downloading one or multiple images from text prompts.

> Disclaimer: This community plugin is created by Dify enthusiasts and is not officially maintained by ByteDance.

## Features

- Use Doubao Seedream 4.0 (`doubao-seedream-4-0-250828`) for text-to-image
- Configurable output sizes (e.g., `2048x2048`, `2560x1440`)

### 1. Text-to-Image

- High-quality image generation from textual descriptions
- Multiple aspect ratios: Square (1024×1024), Portrait (1024×1792), Landscape (1792×1024)
- Multi-image generation in one request
- Direct image download after generation

## Get Started

### Prerequisites
- Access to the Dify platform
- Volcano Engine account with Seedream 4.0 service enabled

### Step 1: Get API Key
1. Visit the Ark Console: `https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey`
2. Create an account or sign in
3. Navigate to "Service Enablement > Vision Foundation Models" and enable Seedream 4.0 (comes with 200 free generations)
4. Generate your API Key in the console

### Step 2: Install the Plugin
1. Open the Dify Plugin Marketplace
2. Search for "Doubao Seedream 4.0"
3. Click "Install" and wait for the installation to complete

### Step 3: Configure Authorization
1. In Dify, go to `Plugins > Doubao Seedream 4.0 > API Key Configuration`
2. Enter your Volcano Engine API Key
3. Save the configuration

### Step 4: Start Using
After API Key configuration, you can start using the plugin.

### Step 5: Prompt Examples
```
Single image: "A girl with long golden hair, golden eyes, and a golden dress"
Multiple images: "I need 4 comic panels telling the story of an adventurer exploring a forest"
```

### Tips
- Choose an appropriate aspect ratio based on your use case

### FAQ
- Invalid API Key: Verify your Volcano Engine API Key and service permissions
- Generation failed: Check whether your prompt complies with content policies
- Slow response: Peak periods may cause delays; please try again later

## Contributing

We welcome feedback and contributions! You can:
- Report bugs and issues
- Propose new features
- Open pull requests
- Improve documentation

## Privacy

See `PRIVACY.md` / `PRIVACY.zh-Hans.md` for details.

## License

This project follows the license terms specified in the `LICENSE` file.

---

Created by Skylineneon
