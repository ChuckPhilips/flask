FROM python:2.7
RUN mkdir /app
COPY ./app.py /app
COPY ./requirements.txt /app
COPY ./templates /app/templates
COPY ./static /app/static
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5002
ENTRYPOINT ["python"]
CMD ["app.py"]
