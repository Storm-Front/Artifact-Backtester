FROM python:3.11.3-slim AS backtester
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y gcc g++ libffi-dev
RUN pip3 install --upgrade pip


WORKDIR /tmp
COPY requirements.txt .
RUN  pip3 install -r requirements.txt

WORKDIR /app


CMD ["bash","start.sh"]