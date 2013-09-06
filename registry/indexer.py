import signals


def tag_created_handler(sender):
    pass


def tag_deleted_handler(sender):
    pass


def subscribe():
    signals.tag_created.connect(tag_created_handler)
    signals.tag_deleted.connect(tag_deleted_handler)
