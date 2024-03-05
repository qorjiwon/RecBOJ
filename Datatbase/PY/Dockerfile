FROM python:3.9 

RUN pip install psycopg2-binary

COPY . . 

CMD ["create_table.py"]

ENTRYPOINT ["python3"]