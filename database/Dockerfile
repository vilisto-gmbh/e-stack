FROM timescale/timescaledb:latest-pg18

HEALTHCHECK --interval=5s --timeout=30s --retries=3 --start-period=5s CMD ["sh", "-c", "psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
