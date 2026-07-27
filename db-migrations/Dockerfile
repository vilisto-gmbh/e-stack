FROM sqitch/sqitch:latest

ENV DEFAULT_USER="james_prescott_joule"

USER root

RUN mkdir -p /tmp/sqitch-init \
    && useradd --no-create-home --home /tmp/sqitch-init --uid 1000 $DEFAULT_USER \
    && apt update \
    && apt upgrade -y \
    && apt-get install --only-upgrade linux-libc-dev --no-install-recommends

COPY --chown=${DEFAULT_USER} ./src/ /tmp/sqitch-init/
RUN chmod +x /tmp/sqitch-init/trigger-job.sh

USER $DEFAULT_USER
WORKDIR /tmp/sqitch-init

ENTRYPOINT exec /tmp/sqitch-init/trigger-job.sh