import dagster as dg

etl_pipeline_example = dg.define_asset_job(
    name="etl_pipeline_example",
    selection=["raw_data", "prediction_data", "ingest_prediction_data"],
)
