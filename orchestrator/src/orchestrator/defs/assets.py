import bambi as bmb
import pandas as pd
import dagster as dg
from typing import Any
from .resources import PostgrestConnector


@dg.asset
async def raw_data(
    context: dg.AssetExecutionContext, postgrest: PostgrestConnector
) -> Any:
    data_dict = await postgrest.get_json_async(suburl="energy_data")
    context.log.info(f"Extracted dict with {len(data_dict)} entries.")
    return data_dict


@dg.asset(
    deps=["raw_data"],
)
def prediction_data(
    context: dg.AssetExecutionContext,
    raw_data: Any,
) -> pd.DataFrame:

    data_df = pd.DataFrame(raw_data)
    context.log.info(f"Transformed raw data into a dataframe of length {len(data_df)}.")

    model = bmb.Model("power ~ th_amb + th_amb_prev_day + is_workday", data_df)
    context.log.info(f"Created the following Bayesian Model: {model}")

    inf_data = model.fit(chains=2)
    context.log.info("Model fitting complete.")

    model.predict(inf_data, inplace=True, kind="response")
    context.log.info("Prediction complete.")

    post_pred = inf_data.posterior_predictive["power"]
    pred_df = data_df.assign(
        power_pred=post_pred.mean(dim=("chain", "draw")).values,
        power_pred_lo=post_pred.quantile(0.1, dim=("chain", "draw")).values,
        power_pred_hi=post_pred.quantile(0.9, dim=("chain", "draw")).values,
    )
    context.log.info("Computation of power complete.")
    context.add_output_metadata(
        {
            "num_rows": len(pred_df),
            "processed_df": dg.MetadataValue.md(f"````\n{pred_df.head(3)}\n```"),
        }
    )

    return pred_df


@dg.asset(deps=["prediction_data"])
async def ingest_prediction_data(
    context: dg.AssetExecutionContext,
    prediction_data: pd.DataFrame,
    postgrest: PostgrestConnector,
) -> None:

    pred_data_json = prediction_data.to_dict(orient="records")
    pgrst_rsp = await postgrest.upsert_async(
        suburl="energy_data",
        json=pred_data_json,
        on_conflict="time",
    )
    context.log.info(
        f"Data ingest terminated with status code {pgrst_rsp.status_code}."
    )
