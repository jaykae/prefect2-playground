FROM prefecthq/prefect:2.11.0-python3.11

RUN pip install prefect-docker prefect-dask && \
    prefect work-pool create docker-agent -t docker

CMD ["prefect", "agent", "start", "-p", "docker-agent", "-q", "main"]