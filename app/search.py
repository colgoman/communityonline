from flask import current_app

def add_to_index(index, model):
    '''
    Build the document to be inserted into the index from the __searchable__ class variable.
    '''
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    # id field used as unique identifier for document
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    '''
    Delete document stored under the provided id
    '''
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    '''
    Take the index name and text to search for with pagination controls.

    '''
    if not current_app.elasticsearch:
        print("EMPTY ERROR")
        return [], 0
    
    # multi match query to search across multiple fields
    # field name of * looks in all fields i.e. the entire index
        # used to make the function generic as different models can have different field names in the index
    search = current_app.elasticsearch.search(
        index=index,
        # from and size arguments control subset of result set needs to be returned
            # elasticsearch does not provide nice pagination object so pagination math must be calculated
        body={'query': {'multi_match': {'query':query, 'fields':['*']}},
                'from':(page - 1)* per_page, 'size': per_page})

    # get index ids and total number of results from search function
    ids = [int(hit['_id']) for hit in search['hits']['hits']]

    # two values are returned
        # (1) list of id elements for the search results
        # (2) total number of results
    return ids, search['hits']['total']['value']






