FROM python:3.13.0-slim-bullseye

ARG PIP_ENVIRONMENT
ARG RUNNER

ENV RUNNER $RUNNER
ENV PYTHONUNBUFFERED 1
ENV TZ="Europe/Moscow"

COPY app/build/pip/ /var/app/build/pip/
RUN cd /var/app/ && pip install -r "build/pip/${PIP_ENVIRONMENT}_requirements.txt"

COPY app/src /var/app/src/

VOLUME /var/app/
WORKDIR /var/app/src/
COPY --chmod=777 ["ci/docker/python/scripts/start-app", "ci/docker/python/scripts/entrypoint", "/" ]

CMD ["/entrypoint"]
