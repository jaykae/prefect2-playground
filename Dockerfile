FROM prefecthq/prefect:2.11.0-python3.11
COPY requirements.txt /opt/prefect/requirements.txt
RUN python -m pip install -r /opt/prefect/requirements.txt
WORKDIR /opt/prefect/
