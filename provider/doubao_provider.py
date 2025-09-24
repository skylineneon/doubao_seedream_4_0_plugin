from typing import Any

import requests
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class ModelScopeProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证 ModelScope API 凭据有效性

        Args:
            credentials: 包含 ModelScope API key 的字典

        Raises:
            ToolProviderCredentialValidationError: 当凭据验证失败时
        """
        try:
            # 检查 API key 是否存在
            api_key = credentials.get("api_key")
            if not api_key:
                raise ToolProviderCredentialValidationError("Doubao API key 不能为空")
            # 检查api key 长度
            if len(api_key) < 36:
                raise ToolProviderCredentialValidationError("Doubao API key 长度不正确")
            # 验证api key 有效性
            # self._test_doubao_connection(api_key)

        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"Doubao API 凭据验证失败: {str(e)}"
            )

    def _test_doubao_connection(self, api_key: str) -> None:
        """
        验证 Doubao API 有效性

        Args:
            api_key: Doubao API key
        """
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": "doubao-1-5-pro-32k-250115",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"},
            ],
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
        except requests.RequestException as req_err:
            raise ToolProviderCredentialValidationError(
                f"无法连接 Doubao 服务: {req_err}"
            )

        if response.status_code != 200:
            # 尝试读取错误信息
            try:
                data = response.json()
                error_message = (
                    data.get("error", {}).get("message")
                    or data.get("message")
                    or response.text
                )
            except Exception:
                error_message = response.text
            raise ToolProviderCredentialValidationError(
                f"Doubao API 响应异常，状态码 {response.status_code}: {error_message}"
            )

        # 基础校验返回结构
        try:
            data = response.json()
            print(data)
        except ValueError:
            raise ToolProviderCredentialValidationError("Doubao API 返回了非 JSON 响应")

        choices = data.get("choices")
        if not isinstance(choices, list) or len(choices) == 0:
            raise ToolProviderCredentialValidationError(
                "Doubao API 返回结果不包含有效的 choices 字段"
            )

        # 如果走到这里，说明 API Key 有效
