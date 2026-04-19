from typing import Dict, Tuple


class FrontmatterService:
    def split(self, text: str) -> Tuple[Dict[str, str], str]:
        if not text.startswith("---\n"):
            return {}, text

        parts = text.split("\n---\n", 1)
        if len(parts) != 2:
            return {}, text

        raw_frontmatter = parts[0][4:]
        body = parts[1]
        data: Dict[str, str] = {}
        for line in raw_frontmatter.splitlines():
            if not line.strip() or ":" not in line:
                continue
            key, value = line.split(":", 1)
            cleaned = value.strip().strip('"')
            if cleaned in {"null", "None", ""}:
                cleaned = ""
            data[key.strip()] = cleaned
        return data, body
