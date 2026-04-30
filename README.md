# Intro

IMPORTANT: Parts of this software are being filed for patent, registration number 24176723.5: "Method, System and Computer Program
for Determining an Efficiency of an Energy-Saving Measure in Buildings".

# Setup

# Services

## database
Uses a [timescale](https://timescale.readthedocs.io/en/latest/) SQL database.

## db-interface
Uses [postgREST](https://docs.postgrest.org/en/v14/) as an interface to the database.

## db-migrations
Uses [sqitch](https://sqitch.org/docs/) for database management and version control. 

## frontend
Uses a [grafana](https://grafana.com/docs/) frontend.

## orchestrator
Uses [dagster](https://docs.dagster.io/) for job orchestration.