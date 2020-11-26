from invoke import Collection, task
from opstrich.invoke import check, openssl


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
    openssl.decrypt(c, "zappa_settings.json")
    deploy(c)


namespace = Collection(check, openssl, deploy, ci_deploy)
