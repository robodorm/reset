FROM lootbox/resetapp:base

WORKDIR /app

ADD . .
RUN pip install . --upgrade
