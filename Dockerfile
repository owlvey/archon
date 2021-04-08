FROM python:3.9.2
WORKDIR /deployment
COPY . .

RUN pip install -r  ./requirements.txt

ENV PYTHONPATH=/deployment
EXPOSE 5000/tcp
ENTRYPOINT ["python", "./startup.py"]