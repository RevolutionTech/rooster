from invoke import task


@task
def check(c):
    """
    Perform all checks.
    """
    c.run("pyupgrade --py38-plus $(find . -name '*.py')")
    c.run("isort . --check")
    c.run("black . --check")
    c.run("./manage.py makemigrations --check")  # validate no outstanding model changes


@task
def deploy(c):
    """
    Build and run a Docker container to deploy.
    """
    c.run("docker build -t zappa-lambda .")
    c.run("docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY zappa-lambda")
    c.run(
        "DJANGO_CONFIGURATION=ProdCollectStaticConfig poetry run python manage.py collectstatic --noinput"
    )


@task
def ci_deploy(c):
    """
    Perform pre-deploy steps needed in CI and then deploy.
    """
    c.run(
        "curl -L "
        "https://github.com/FlipperPA/django-s3-sqlite/blob/8ca00ae642655389fe62ed619db8671ca9910943"
        "/shared-objects/python-3-8/_sqlite3.so?raw=true "
        "--create-dirs -o lib/_sqlite3.so"
    )
    c.run(
        "openssl aes-256-cbc -k $DECRYPT_PASSWORD -in zappa_settings.json.enc -out zappa_settings.json -d"
    )
    deploy(c)
