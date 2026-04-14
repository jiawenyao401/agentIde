import httpx


class BrowserTool:
    def fetch(self, url: str) -> str:
        with httpx.Client(timeout=10) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text[:3000]
