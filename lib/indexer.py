from ..indexer import session, Repository, Tag # FIXME probably doesnt work

def add_repository(name):
	obj = Repository(name=name)
	session.add(obj)
	session.commit()

def add_tag(name, repository_name):
	repo = session.query(Repository, Repository.id).
			filter(Repository.name==repository_name).
			one()
	obj = Tag(name=name, repo_id=repo.id)
	session.add(obj)
	session.commit()

def clear_index():
    session.execute(Repository.delete())
    session.execute(Tag.delete())
    session.commit()