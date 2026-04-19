from typing import Any, Dict, Tuple

import yaml


class FrontmatterService:
    def split(self, text: str) -> Tuple[Dict[str, Any], str]:
        if not text.startswith("---\n"):
            return {}, text

        end = text.find("\n---\n", 4)
        if end == -1:
            return {}, text

        raw_frontmatter = text[4:end]
        body = text[end + 5:]

        try:
            data = yaml.safe_load(raw_frontmatter) or {}
            if not isinstance(data, dict):
                data = {}
        except yaml.YAMLError:
            data = {}

        return data, body
