import indexer
import signals
import toolkit

from .app import app


def tag_created_handler(sender, **kw):
    repo_name = kw['repository']
    tag_name = kw['tag']
    if not indexer.has_repository(repo_name):
        indexer.add_repository(repo_name)
    indexer.add_tag(tag_name, repo_name)


def tag_deleted_handler(sender, **kw):
    indexer.remove_tag(kw['tag'])


def subscribe():
    signals.tag_created.connect(tag_created_handler)
    signals.tag_deleted.connect(tag_deleted_handler)


@app.route('/v1/indexer/<path:repository>/tags',
           methods=['GET'])
def get_tags(repository):
    lst = indexer.list_tags(repository)
    for i in xrange(len(lst)):
        lst[i] = lst[i].to_dict()
    return toolkit.response(lst)


@app.route('/v1/indexer/repositories',
           methods=['GET'])
def get_repositories():
    lst = indexer.list_repositories()
    for i in xrange(len(lst)):
        lst[i] = lst[i].to_dict()
    return toolkit.response(lst)

subscribe()
