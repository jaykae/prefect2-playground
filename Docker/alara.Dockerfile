FROM prefecthq/prefect:2.11.0-python3.11

ARG PREFECT_API_URL

ENV PREFECT_API_URL ${PREFECT_API_URL}

COPY requirements.txt .

RUN pip install -r requirements.txt && mkdir /flows

WORKDIR /flows

COPY ../flows/*.py /flows