FROM python:3.11.2

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY . /opt/app

WORKDIR /opt/app/social_network

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["python", "manage.py", "runserver", "0:8000"]
