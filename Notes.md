# Things attempted

- Docker Compose setup
  - Able to get everything (postgres DB, server, worker) working quickly and easily with compose
  - Shared the host docker socket into the worker just fine
  - Could not get them working on the same network as the worker was creating runs in the default network and not the compose network.  Might be a lack of my understanding but it was also a problem with the UI not saving those fields
  - Even directly calling the REST API would not save the fields, so it seems like there is more work to do on this from the prefect side (or maybe a good docker compose hack I missed)

- Agents vs Workers
  - Coming from Prefect 1, this was a headache to figure out and I wasted a lot of time trying to get an agent to deploy a flow in an image
  - The disconnect between the options is also a bit annoying

- Caching
  -  This was fun to play with, but does not work well inside a docker container.  The cache key is stored in the server and the actual cached file does not persist between runs.  Would have to cache to remote storage
  -  Currently prefect will error out if a cached item cannot be found instead of just recomputing it, apparently on the roadmap someday
 
- Artifacts
  - Easy enough to use, but everything has to be converted to something Pydantic serializable which defaults to using the standard json library which does not handle dates well.  Would like to see if there is a way to implement a different serializer/deserializer as orjson/ujson python libs support datetime conversion

# Future Things to Play with
- K8S deployment
- Local development setup (I really want to figure out compose)
- Task level concurrency and what happens where there are too many tasks in a queue
- Blocks in general
- prefect.yaml, it's newer and a lot of the documentation is still lacking on the best way to use it
- DASK!
  - Dask in K8S long running cluster
  - Dask in a container for optimizing long processes
  - Data transformation tasks
