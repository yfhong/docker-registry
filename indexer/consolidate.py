#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join('..', 'lib'))

import indexer
import models
import storage


def run_consolidate():
    indexer.clear_index()
    store = storage.load()
    basedir = store.repositories
    for ns in store.list_directory(basedir):
        ns = ns.split('/').pop()
        for repo in store.list_directory('{0}/{1}'.format(basedir, ns)):
            repo = repo.split('/').pop()
            repo_name = '{0}/{1}'.format(ns, repo)
            indexer.add_repository(repo_name)
            for tag in store.list_directory(store.tag_path(ns, repo)):
                tag = tag.split('/').pop()
                if tag.startswith('tag_'):
                    tag = tag[4:]
                    indexer.add_tag(tag, repo_name)

if __name__ == "__main__":
    models.Base.metadata.create_all(models.engine)
    run_consolidate()
