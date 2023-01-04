FROM python:3.8

COPY requirements.txt /tmp
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

COPY . /src
WORKDIR /src

# RUN ["python3", "-u", "main.py"]
