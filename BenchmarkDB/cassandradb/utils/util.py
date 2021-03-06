import time

from cassandra.cqlengine.query import Token

from BenchmarkDB.cassandradb.utils.database import _manager
from BenchmarkDB.cassandradb.utils._cassandra import DocumentModel

_manager.setup()
# logger = logging.getLogger(__name__)


def documents(*sources):
    """fooo"""

    # ipdb.set_trace()

    docs = []
    q = DocumentModel.objects.timeout(500).allow_filtering().all().limit(1000)
    querysets = (q.filter(source=source) for source in sources) if sources else [q]
    for query in querysets:
        page = try_forever(list, query)
        while len(page) > 0:
            for doc in page:
                docs.append(doc)
                # yield doc
            page = try_forever(next_page, query, page)

def next_page(query, page):
    return list(query.filter(pk__token__gt=Token(page[-1].pk)))


def try_forever(action, *args, **kwargs):
    while True:
        try:
            return action(*args, **kwargs)
        except Exception as e:
            # logger.exception(e)
            time.sleep(5)
            # logger.info("Trying again...")
