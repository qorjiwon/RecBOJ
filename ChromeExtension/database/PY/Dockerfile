FROM --platform=linux/amd64 python:3.9 

RUN pip install psycopg2-binary
RUN pip install pandas==2.2.1
COPY . . 

CMD ["create_table.py"]

ENTRYPOINT ["python3"]