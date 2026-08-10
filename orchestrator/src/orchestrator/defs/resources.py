import os
import httpx
import pandas as pd
import dagster as dg
from typing import Any
from .utils import HttpConnector

class PostgrestConnector(dg.ConfigurableResource):
    """A python client for http requests to a postgREST interface."""

    base_url: str
    ca_file: str | None = None
    cert_file: str | None = None
    key_file: str | None = None
    
    @property
    def http_connector(self) -> HttpConnector:
        return HttpConnector(
            base_url=self.base_url,
            ca_file=self.ca_file,
            cert_file=self.cert_file,
            key_file=self.key_file,
        )

    async def get_json_async(self, suburl: str, params: dict | None = None) -> Any:
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
            raise httpx.HTTPError(message=f"Received code {resp.status_code}: {resp.text}.")

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
            raise httpx.HTTPError(
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
            raise httpx.HTTPError(
                f"Received postgREST error code {err["code"]} with message '{err["message"]}'."
            )

@dg.definitions
def resources():
    return dg.Definitions(
            resources={
                "postgrest": PostgrestConnector(
                    base_url=f"http://{os.getenv('POSTGREST_HOST')}:{os.getenv('PGRST_SERVER_PORT')}"
                    )
                }
            )
