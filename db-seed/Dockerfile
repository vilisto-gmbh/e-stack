FROM alpine/psql:18.4

RUN mkdir -p /src/data \
    && mkdir /temp_data
COPY --chmod=+x ./seed_db.sh /src
COPY ./data/sample_data.csv /src/data

WORKDIR /src
ENTRYPOINT ["sh", "seed_db.sh"]
