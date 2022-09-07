FROM python:3.8-alpine

COPY requirements.txt .

RUN pip3.8 install --upgrade pip \
    && pip3.8 install -r requirements.txt \
    && rm requirements.txt

COPY . .