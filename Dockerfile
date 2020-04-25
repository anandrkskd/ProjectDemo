FROM python
COPY . /app
WORKDIR /app
RUN pip3 install -r rq.txt 
ENTRYPOINT ["python"]
CMD ["app.py"]