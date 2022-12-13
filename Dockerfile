FROM python:3.8-buster as build

COPY . .
RUN pip install -U --no-cache-dir pip poetry setuptools wheel && \
    poetry build -f wheel && \
    poetry export -f requirements.txt -o requirements.txt --without-hashes && \
    pip wheel -w dist -r requirements.txt


FROM python:3.8-slim-buster as runtime

WORKDIR /usr/src/app

ENV PYTHONOPTIMIZE true
ENV DEBIAN_FRONTEND noninteractive
ENV GUNICORN_WORKERS 2

# setup timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install gdown && \
    # .env
    gdown --id '16QLx6X60yixKstVFLEnwZBHxgjiThVxD' && \
    # cold_reco
    gdown --id '1SAhZjDdoO8SdiM4aRojsi-1sHpLSmTDi' && \
    # item_dataset
    gdown --id '1pNBUY3SUJCOfwBbYQsGzpum-NwO5caaT' && \
    # user_dataset
    gdown --id '1gMfP4iaSDK2cbXx--o4fuHWtc_s7Qswj'

COPY --from=build dist dist
COPY --from=build main.py gunicorn.config.py service/db/fill_index.py .env ./


RUN apt-get update && \
    apt-get install libgomp1 && \
    pip install -U --no-cache-dir pip dist/*.whl && \
    rm -rf dist

CMD ["python", "fill_index.py"]
CMD ["gunicorn", "main:app", "-c", "gunicorn.config.py"]
