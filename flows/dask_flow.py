from datetime import timedelta

import requests
from prefect import flow, get_run_logger, task
from prefect.tasks import task_input_hash


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=5))
def get_data(url: str) -> dict:
    pass


@task
def filter_data(data: dict) -> dict:
    pass


@task
def persist_results(data: dict, location: str):
    pass


@flow(name="Dask Flow")
def dask_flow(url: str, location: str):
    raw_data = get_data(url)
    filtered_data = filter_data(raw_data)
    persist_results(filtered_data)
