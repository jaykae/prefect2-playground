# pylint: disable=W1203,W4902,W3101

import json
from datetime import datetime, timedelta

import requests
from prefect import flow, get_run_logger, task
from prefect.artifacts import create_table_artifact
from prefect.tasks import task_input_hash


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=60))
def get_data(url: str) -> dict:
    logger = get_run_logger()
    logger.info(f"Attempting to download {url}")
    result = requests.get(url)
    data = result.json()
    if len(data) > 0:
        logger.info("Successfully downloaded the data")
    else:
        logger.warn("Request successful but no data was returned")

    return data


@task
def filter_data(data: dict) -> dict:
    logger = get_run_logger()

    logger.info(f"Beginning to parse the data which has {len(data)} records")

    results = {}
    for record in data:
        actor = record["actor"]["login"]
        action = record["type"]
        action_time = datetime.strptime(record["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        last_action_time = (
            results.get(actor, {}).get(action, {}).get("last_action", None)
        )
        first_action_time = (
            results.get(actor, {}).get(action, {}).get("first_action", None)
        )
        action_count = results.get(actor, {}).get(action, {}).get("count", 0)

        updated_record = {
            actor: {
                action: {
                    "last_action": (
                        action_time
                        if last_action_time is None or last_action_time < action_time
                        else last_action_time
                    ),
                    "first_action": (
                        action_time
                        if first_action_time is None or first_action_time < action_time
                        else first_action_time
                    ),
                    "count": action_count + 1,
                }
            }
        }

        results.update(updated_record)

    logger.info("Completed parsing the data, reformatting")

    output = []
    for actor in results:
        for action in results[actor]:
            output.append({"actor": actor, "action": action, **results[actor][action]})

    output.sort(key=lambda x: x["count"], reverse=True)

    return output


@task
def persist_results(data: dict, artifact_name: str):
    json.dumps(data, default=str)
    create_table_artifact(
        table=json.loads(json.dumps(data, default=str)),
        key=artifact_name,
        description="Github activity sorted by most performed functions",
    )


@flow(name="Standard Flow")
def standard_flow(
    url: str = "https://github.com/json-iterator/test-data/raw/master/large-file.json",
    artifact_name: str = None,
):
    raw_data = get_data(url)
    filtered_data = filter_data(raw_data)
    persist_results(filtered_data, artifact_name)


if __name__ == "__main__":
    standard_flow()
