FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /code

COPY . /code/

WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["python", "chattr/manage.py", "runserver", "0.0.0.0:8000"]

