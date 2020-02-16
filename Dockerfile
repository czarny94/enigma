FROM python:3.8-alpine

WORKDIR /usr/src/enigma

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY dist/enigma-0.1.0-py3-none-any.whl ./
RUN pip install --target=./ ./enigma-0.1.0-py3-none-any.whl && \
    rm ./enigma-0.1.0-py3-none-any.whl

CMD python -m enigma
