import httpx
from ssl import Purpose, create_default_context

class HttpConnector:
    def __init__(
        self,
        base_url: str,
        ca_file: str | None = None,
        cert_file: str | None = None,
        key_file: str | None = None,
    ):
        self.base_url = base_url
        self.ctx = None
        if all([ca_file is not None, cert_file is not None, key_file is not None]):
            self.ctx = create_default_context(purpose=Purpose.SERVER_AUTH, cafile=ca_file)
            self.ctx.load_cert_chain(
                certfile=cert_file,
                keyfile=key_file,
            )

    async def get_json_async(self, suburl: str, headers: dict, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(verify=self.ctx) as a_client:
            resp = await a_client.get(
                url=f"{self.base_url}/{suburl}", headers=headers, params=params
            )

        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            raise httpx.HTTPError(message=f"Received code {resp.status_code}: {resp.text}.")

    async def post_json_async(
        self,
        suburl: str,
        headers: dict,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
    ) -> httpx.Response:
        async with httpx.AsyncClient(verify=self.ctx) as a_client:
            resp = await a_client.post(
                url=f"{self.base_url}/{suburl}",
                headers=headers,
                json=json,
                params=params,
                data=data,
            )

        return resp

