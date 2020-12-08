FROM ubuntu
RUN apt-get update -y && \
    apt-get upgrade -y
RUN apt-get install -y imagemagick
RUN apt-get install -y \
    python3.7 \
    python3-pip

COPY requirements.txt /app/requirements.txt
WORKDIR app
RUN pip3 install --user -r requirements.txt

COPY . /app
CMD ["make_gifs.py"]
ENTRYPOINT ["python3"]