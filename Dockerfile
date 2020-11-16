# Derived from: https://romandc.com/zappa-django-guide/setup/#approach-2-docker-with-zappa-recommended
FROM lambci/lambda:build-python3.8

WORKDIR /var/task

COPY . .

RUN poetry install --no-dev

CMD ["poetry", "run", "zappa", "update"]
