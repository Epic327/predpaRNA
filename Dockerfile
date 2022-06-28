FROM tensorflow/tensorflow:2.3.0

RUN pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 4000


ENTRYPOINT  ["python"]

CMD ["app.py"]
