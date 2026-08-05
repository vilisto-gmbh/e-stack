-- Deploy 20260729111320_example_1.sql to pg --

CREATE TABLE app_schema.energy_data (
  time TIMESTAMP WITH TIME ZONE,
  power FLOAT,
  power_unit VARCHAR,
  energy FLOAT,
  energy_unit VARCHAR,
  th_amb FLOAT,
  is_workday BOOLEAN,
  power_pred FLOAT
);
