FROM arm32v6/python:3.8-alpine

RUN apk --no-cache --update-cache add py3-numpy-dev openblas-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY clash_stats .

CMD celery -A clash_stats.tasks worker -B
