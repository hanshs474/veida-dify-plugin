from typing import Any

from dify_plugin import ToolProvider


class VeidaProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """Nothing to validate.

        Veida's anonymous tier needs no key, which is the whole point of this
        provider: it works on install. Raising here would block a setup that is
        already correct.
        """
        return
