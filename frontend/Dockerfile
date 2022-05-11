FROM python:3.9

COPY ./app.py /frontend
COPY ./requirements.txt /frontend

WORKDIR /frontend

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]