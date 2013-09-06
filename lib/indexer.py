import models


def add_repository(name):
    obj = models.Repository(name=name)
    models.session.add(obj)
    models.session.commit()


def add_tag(name, repository_name):
    repo = models.session.query(models.Repository, models.Repository.id).\
        filter(models.Repository.name == repository_name).\
        one()
    obj = models.Tag(name=name, repo_id=repo.id)
    models.session.add(obj)
    models.session.commit()


def clear_index():
    models.session.execute(models.Repository.delete())
    models.session.execute(models.Tag.delete())
    models.session.commit()
