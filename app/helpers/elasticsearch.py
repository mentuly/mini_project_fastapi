# from typing import Optional
# from .. import es


# def search_in_elasticsearch(
#     category: Optional[str], min_price: Optional[float], max_price: Optional[float]
# ):
#     query_body = {
#         "query": {
#             "bool": {
#                 "must": [
#                     {"match": {"category": category}} if category else {},
#                     {"range": {"price": {"gte": min_price}}} if min_price else {},
#                     {"range": {"price": {"lte": max_price}}} if max_price else {},
#                 ]
#             }
#         }
#     }

#     result = es.search(index="ads", body=query_body)

#     return result["hits"]["hits"]