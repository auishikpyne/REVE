FROM alpine:latest
RUN apk add cmd:pip3 \
    && apk add --no-cache python3-dev \
    && pip3 install --upgrade pip
# setting a directory for the app
WORKDIR /app

# copy all the files to the container
COPY . /app

# install dependencies
RUN pip3 --no-cache-dir install -r requirements.txt

#defining  the port number the container should expose 
EXPOSE 5000

#ENTRYPOINT ["python3"]
CMD ["python3","app.py"]

