FROM sqitch/sqitch:latest

ARG DB_USER

USER root

RUN mkdir -p /tmp/sqitch-init \
    && useradd --no-create-home --home /tmp/sqitch-init --uid 1000 $DB_USER \
    && apt update \
    && apt upgrade -y \
    && apt-get install --only-upgrade linux-libc-dev --no-install-recommends

COPY --chown=${DB_USER} ./src/ /tmp/sqitch-init/
RUN chmod +x /tmp/sqitch-init/trigger-job.sh

USER $DB_USER
WORKDIR /tmp/sqitch-init

ENTRYPOINT exec /tmp/sqitch-init/trigger-job.sh
