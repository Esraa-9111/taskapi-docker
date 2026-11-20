
FROM python:3.14


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt  


COPY . .

COPY ./main.py ./connect_with_db.py ./


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]