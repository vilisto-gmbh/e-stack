FROM timescale/timescaledb:latest-pg18

COPY init_scripts/* /docker-entrypoint-initdb.d/
COPY entrypoint.sh /usr/local/bin/custom-entrypoint.sh
RUN chmod +x /usr/local/bin/custom-entrypoint.sh

HEALTHCHECK --interval=5s --timeout=30s --retries=3 --start-period=5s CMD ["sh", "-c", "psql -U postgres -d app_db"]

ENTRYPOINT ["custom-entrypoint.sh"]
CMD ["postgres"]
