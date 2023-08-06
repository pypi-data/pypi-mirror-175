FROM python:3.10.7

WORKDIR /docs
RUN pip3 install pdoc
# COPY . .


CMD ["pdoc", "./classes.py", "-h", "0.0.0.0", "-p", "8912"]
