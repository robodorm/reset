.PHONY: app base docker4compose tests-functional tests-unit

base:
	-docker build . -f Dockerfile.base -t lootbox/resetapp:base

app:
	-docker build . -f Dockerfile.app -t lootbox/resetapp:app

tests-functional:
	-cd tests/functional && pyresttest http://localhost crud.yml

tests-unit:
	-cd tests/unit && python -m unittest


# PROD BUILDS
a: app
b: base

# RUN TESTS (inside app container)
ut: tests-unit
ft: tests-functional

all: base app
