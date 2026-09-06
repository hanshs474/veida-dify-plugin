from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._client import VeidaError, run


class GenerateImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        prompt = (tool_parameters.get("prompt") or "").strip()
        if not prompt:
            yield self.create_text_message("prompt is required")
            return
        ratio = tool_parameters.get("aspect_ratio") or "1:1"
        try:
            url = run(prompt, aspect_ratio=ratio)
        except VeidaError as err:
            yield self.create_text_message(f"Veida: {err}")
            return
        yield self.create_image_message(url)
        yield self.create_text_message(url)
