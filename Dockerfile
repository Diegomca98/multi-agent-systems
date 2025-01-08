FROM python:3.10-slim

COPY requirements.txt /tmp/requirements.txt

COPY src /src
COPY .env /.env

WORKDIR /

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /py \
    && /py/bin/pip install --upgrade pip \
    && /py/bin/pip install -r /tmp/requirements.txt \
    && rm -rf /tmp
    
ENV PATH="/py/bin:$PATH"

CMD ["streamlit", "run", "--server.port", "8501", "/src/main.py"]