FROM python:3.9 

RUN pip install psycopg2-binary
RUN pip install pandas==2.2.1
RUN pip install requests

COPY . . 

CMD ["create_table.py"]

ENTRYPOINT ["python3"]