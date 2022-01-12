FROM python:3.9

# FROM arm32v6/python:3.8-alpine  # For raspberry pi
# RUN apk --no-cache --update-cache add py3-numpy-dev openblas-dev

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY clash_api ./clash_api
COPY clash_stats ./clash_stats

CMD PYTHONPATH=. celery -A clash_stats.tasks worker -B
