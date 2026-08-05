import httpx
import pandas as pd
from httpx import HTTPError
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
            raise HTTPError(message=f"Received code {resp.status_code}: {resp.text}.")

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

class PostgrestConnector:
    """A python client for http requests to a postgREST interface."""

    def __init__(
        self,
        base_url: str,
        ca_file: str | None = None,
        cert_file: str | None = None,
        key_file: str | None = None,
    ):
        self.http_connector = HttpConnector(
            base_url=base_url, ca_file=ca_file, cert_file=cert_file, key_file=key_file
        )

    async def get_json_async(self, suburl: str, params: dict | None = None) -> dict:
        """Gets data from a table. Refer to https://docs.postgrest.org/en/v12/references/api/tables_views.html for filtering syntax."""

        resp = await self.http_connector.get_json_async(
            suburl=suburl, headers={"accept": "application/json"}, params=params
        )
        return resp

    async def upsert_async(
        self, suburl: str, json: dict, on_conflict: str | None = None
    ) -> httpx.Response:
        params = {"on_conflict": on_conflict} if on_conflict is not None else None
        resp = await self.http_connector.post_json_async(
            headers={"Prefer": "resolution=merge-duplicates, return=representation"},
            suburl=suburl,
            params=params,
            json=json,
        )

        if any([resp.status_code == httpx.codes.OK, resp.status_code == httpx.codes.CREATED]):
            return resp
        else:
            raise HTTPError(message=f"Received code {resp.status_code}: {resp.text}.")

    async def insert_pandas_async(self, suburl: str, data: pd.DataFrame) -> httpx.Response:
        resp = await self.http_connector.post_json_async(
            headers={"Content-Type": "text/csv", "Prefer": "return=representation"},
            suburl=suburl,
            data=data.to_csv(index=False, na_rep="NULL"),
        )

        if resp.status_code == httpx.codes.CREATED:
            return resp
        else:
            err = resp.json()
            raise HTTPError(
                message=f"Received PostgREST error code {err["code"]} with message '{err["message"]}' and details '{err["details"]}'."
            )

    async def delete(self, suburl: str, keys: list[int], key_name: str) -> httpx.Response:
        if len(keys) == 1:
            params = f"{key_name}=eq.{keys[0]}"
        else:
            id_str = [str(id) for id in keys]
            params = f"{key_name}=in.({",".join(id_str)})"

        async with httpx.AsyncClient(verify=self.http_connector.ctx) as a_client:
            resp = await a_client.delete(
                url=f"{self.http_connector.base_url}/{suburl}?{params}",
                headers={"Prefer": "return=representation"},
            )

        if resp.status_code == httpx.codes.OK:
            print(f"Successfully ran deletion request, deleted entries are \n {resp.text}.")
            return resp
        else:
            err = resp.json()
            raise HTTPError(
                f"Received postgREST error code {err["code"]} with message '{err["message"]}'."
            )

