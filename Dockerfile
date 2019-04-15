FROM python:3.7-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
RUN apk add tzdata
COPY --from=builder /install /usr/local
COPY src /app
WORKDIR /app
CMD ["python3", "-u", "ncid-relay.py"]
