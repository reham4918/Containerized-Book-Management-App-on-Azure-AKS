FROM python:3.10


COPY . .

RUN pip install flask pymongo gunicorn

EXPOSE 5000

ENTRYPOINT ["gunicorn", "app:app"]

