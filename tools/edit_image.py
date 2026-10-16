from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._client import VeidaError, run


class EditImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        prompt = (tool_parameters.get("prompt") or "").strip()
        image_url = (tool_parameters.get("image_url") or "").strip()
        if not prompt or not image_url:
            yield self.create_text_message("both prompt and image_url are required")
            return
        try:
            url = run(prompt, image_url=image_url)
        except VeidaError as err:
            yield self.create_text_message(f"Veida: {err}")
            return
        yield self.create_image_message(url)
        yield self.create_text_message(url)
