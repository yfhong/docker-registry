import os
import sys

root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root_path, '..', 'indexer_module'))

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


def has_repository(name):
    return models.session.query(models.Repository, models.Repository.id).\
        filter(models.Repository.name == name).\
        count() > 0


def get_tag(name, repository_name):
    repo = models.session.query(models.Repository, models.Repository.id).\
        filter(models.Repository.name == repository_name).\
        one()
    tag = models.sessions.query(models.Tag).\
        filter(models.Tag.repo_id == repo.id).\
        filter(models.Tag.name == name).\
        one()
    return tag


def remove_tag(id):
    models.session.query(models.Tag).filter(models.Tag.id == id).delete()
    models.session.commit()


def list_repositories():
    return models.session.query(models.Repository).all()


def list_tags(repo_name):
    try:
        repo = models.session.query(models.Repository, models.Repository.id).\
            filter(models.Repository.name == repo_name).\
            one()
    except Exception:
        return []
    return models.session.query(models.Tag).\
        filter(models.Tag.repo_id == repo.id).\
        all()


def clear_index():
    models.session.query(models.Repository).delete()
    models.session.query(models.Tag).delete()
    models.session.commit()
