import typing

import httpx

import lib.app.split_settings as app_split_settings


class AsyncHttpClient:
    def __init__(
        self,
        proxy_settings: app_split_settings.ProxySettings,
        base_url: str | None = None,
        **client_params: dict[typing.Any, typing.Any],
    ) -> None:
        self.base_url = base_url if base_url else ""
        self.proxy_settings = proxy_settings
        self.proxies = self._get_proxies_from_settings()
        self.client_params = client_params

        self.client = self._get_client()

    def _get_proxies_from_settings(self) -> dict[str, str] | None:
        if not self.proxy_settings.enable:
            return None
        proxies = {"all://": self.proxy_settings.dsn}
        return proxies

    def _get_client(self):
        return httpx.AsyncClient(
            base_url=self.base_url,
            proxies=self.proxies,  # type: ignore
            **self.client_params,
        )

    async def close(self):
        if not self.client:
            return
        await self.client.aclose()
