#!/usr/bin/env python

import indexer
import storage

def run_consolidate():
	indexer.clear_index()
	store = storage.load()
	basedir = store.repositories
	for ns in store.list_directory(basedir):
		for repo in store.list_directory('{0}/{1}'.format(basedir, ns)):
			repo_name = '{0}/{1}'.format(ns, repo)
			indexer.add_repository(repo_name)
			for tag in store.list_directory(store.tag_path(ns, repo)):
				indexer.add_tag(tag, repo_name)

if __name__ == "__main__":
	run_consolidate()