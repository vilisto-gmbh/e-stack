import polars as pl
import dagster as dg
from pathlib import Path

INPUT_FILE = Path(__file__).parent/"data"/"example_1.csv"

@dg.asset
def processed_csv(context: dg.AssetExecutionContext):
    
    df = pl.scan_csv(INPUT_FILE).with_columns(
        (
            pl.col("power") * pl.col("time").str.to_datetime().diff().dt.total_seconds()/3600
        ).alias("energy"),
        pl.lit("MWh").alias("energy_unit"),
    ).collect()
    context.log.info(
        f"Processing of input file {INPUT_FILE} complete."
    )
    context.add_output_metadata(
        {
            "num_rows": df.height,
            "processed_df": dg.MetadataValue.md(f"````\n{df.head(3)}\n```"),
        }
    )
