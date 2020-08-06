FROM ubuntu:19.10

RUN apt update -y && apt install -y perl sox libsox-fmt-all python3 python3-pip

COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

WORKDIR /app/

EXPOSE 8000

ENTRYPOINT ["python3", "app.py"]
