import requests
import json
import logging
from collections.abc import Generator
from PIL import Image
from io import BytesIO
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool

# 配置日志
logger = logging.getLogger(__name__)


# 配置日志格式和输出
def setup_logging():
    """配置日志输出"""
    # 避免重复配置
    if getattr(setup_logging, "_configured", False):
        return

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式器
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # 配置根日志器（仅当没有处理器时）
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

    # 使用模块 logger，交由根 logger 处理输出，不重复添加处理器
    logger.setLevel(logging.INFO)
    logger.propagate = True
    logger.handlers = []

    # 标记已配置
    setup_logging._configured = True


# 初始化日志配置
setup_logging()


class Text2ImageTool(Tool):
    def _invoke(
        self, tool_parameters: dict
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        基于 火山方舟 Ark Images Generations API 的文生图工具
        参考 `nano_banana` 的交互与错误处理风格，直接同步生成并下载图片。
        """
        logger.info("开始执行豆包文生图任务 (Ark)")

        try:
            # 1) 获取 API 配置
            api_key = self.runtime.credentials.get("api_key")
            if not api_key:
                msg = "API密钥未配置"
                logger.error(msg)
                yield self.create_text_message(msg)
                return

            api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            # 2) 获取与校验参数
            prompt = tool_parameters.get("prompt", "").strip()
            if not prompt:
                msg = "请输入提示词"
                logger.warning(msg)
                yield self.create_text_message(msg)
                return
            size = tool_parameters.get("size", "2048x2048")

            # 进度/调试提示（参考 nano_banana 风格）
            yield self.create_text_message("🤖 豆包文生图启动中...\n")

            # 3) 构建请求载荷（按官方示例）
            payload = {
                "model": "doubao-seedream-4-0-250828",
                "prompt": prompt,
                "size": size,
                "sequential_image_generation": "auto",
                "stream": False,
                "response_format": "url",
                "watermark": False,
            }

            logger.info(f"提交生成请求: {json.dumps(payload, ensure_ascii=False)}")
            yield self.create_text_message("⏳ 正在生成图像，请稍候...\n")

            # 4) 发送请求
            try:
                response = requests.post(
                    api_url,
                    headers=headers,
                    data=json.dumps(payload),
                )
            except requests.exceptions.Timeout:
                msg = "请求超时，请稍后重试"
                logger.error(msg)
                yield self.create_text_message(f"❌ {msg}\n")
                return
            except requests.exceptions.RequestException as e:
                msg = f"请求失败: {str(e)}"
                logger.error(msg)
                yield self.create_text_message(f"❌ {msg}\n")
                return

            # 5) 检查响应
            if response.status_code != 200:
                logger.error(
                    f"API 响应非 200: {response.status_code}, 内容: {response.text[:300]}"
                )
                yield self.create_text_message(
                    f"❌ API 响应状态码: {response.status_code}"
                )
                if response.text:
                    yield self.create_text_message(
                        f"🔧 响应内容: {response.text[:500]}"
                    )
                return

            # 6) 解析响应
            try:
                resp_data = response.json()
            except json.JSONDecodeError as e:
                logger.error(
                    f"解析响应JSON失败: {str(e)} - 原始内容: {response.text[:300]}"
                )
                yield self.create_text_message("❌ API 响应解析失败（非JSON）")
                return

            data_list = resp_data.get("data", [])
            if not data_list:
                yield self.create_text_message("❌ API 响应中未返回图像数据")
                return
            else:
                yield self.create_text_message(f"🎉 图像生成成功，开始下载...\n")
            for i, data in enumerate(data_list):
                yield self.create_text_message(f"开始下载第{i + 1}张图片:")
                image_url = data.get("url", "")
                image_size_text = data.get("size", "")
                if not image_url:
                    yield self.create_text_message(f"❌ 未获取到第{i + 1}张图片的URL")
                    return
                if image_size_text:
                    yield self.create_text_message(
                        f"📐 第{i + 1}张图片尺寸: {image_size_text}"
                    )

                # 7) 下载图像并转 PNG
                try:
                    # img
                    yield self.create_image_message(image_url)
                    yield self.create_text_message(f"✅ 第{i + 1}张图片生成完成！")

                except Exception as e:
                    logger.error(f"下载/处理图像失败: {str(e)}")
                    yield self.create_text_message(f"❌ 下载或处理图像失败: {str(e)}")
                    return

            # 8) 输出使用统计信息（若返回）
            usage = resp_data.get("usage", {})
            if usage:
                if isinstance(usage, dict):
                    yield self.create_json_message(usage)
                else:
                    # 若非字典，降级为文本输出，避免校验错误
                    try:
                        usage_text = json.dumps(usage, ensure_ascii=False)
                    except Exception:
                        usage_text = str(usage)
                    yield self.create_text_message(f"📊 使用信息: {usage_text}")

            logger.info("豆包文生图任务完成")

        except Exception as e:
            error_msg = f"生成图像时出现未预期错误: {str(e)}"
            logger.exception(error_msg)
            yield self.create_text_message(error_msg)
