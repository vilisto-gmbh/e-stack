FROM postgrest/postgrest

USER root
RUN apt-get update\
    && apt-get install -y --no-install-recommends curl
COPY ./postgrest.conf /etc/postgrest.conf

HEALTHCHECK --interval=5s --timeout=30s --retries=3 --start-period=5s CMD ["sh", "-c", "curl -I http://${POSTGREST_HOST}:${PGRST_ADMIN_SERVER_PORT}/live"]

CMD ["postgrest", "/etc/postgrest.conf"]
