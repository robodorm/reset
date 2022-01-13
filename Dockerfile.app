FROM robodorm/resetapp:base

WORKDIR /app

ADD . .
RUN pip install .
