FROM python:3.10.8

WORKDIR /usr/src/Backend/routing_app
RUN pip install --upgrade pip "setuptools<71"
COPY ./Backend/routing_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./Backend/routing_app .
COPY ./AttendancePro ../../AttendancePro
