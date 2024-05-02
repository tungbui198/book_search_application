from owlready2 import get_ontology, default_world


# Load one or more ontologies
go = get_ontology("tool/ontology_with_enrich_data.owl").load()


base_query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://www.semanticweb.org/huutuongtu/ontologies/2024/3/untitled-ontology-15#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>"""


def get_book_by_id_query(id: int):
    query = """
            SELECT ?book_id ?author ?book_title ?book_desc ?publisher ?year ?page ?language
                    WHERE {
                            ?book :hasID "%s" .
                            OPTIONAL {?book :hasID ?book_id} .
                            OPTIONAL {?book :hasTitle ?book_title} .
                            OPTIONAL {?book :hasDescription ?book_desc} .
                            OPTIONAL {?book :hasAuthor ?authorin} .
                            OPTIONAL {?authorin :authorHasName ?author} .
                            OPTIONAL {?book :hasPublisher ?publisherin} .
                            OPTIONAL {?publisherin :publisherHasName ?publisher} .
                            OPTIONAL {?book :hasPublishYear ?year} .
                            OPTIONAL {?book :hasNumberPage ?page} .
                            OPTIONAL {?book :hasLanguage ?languagein} .
                            OPTIONAL {?languagein :languageHasName ?language} .
                            }
        """ % (
        str(id)
    )
    return query


def search_book_query(
    category: str = None,
    title: str = None,
    author: str = None,
    publisher: str = None,
    year: int = None,
    page: int = None,
    language: str = None,
    extension: str = None,
    rate: float = None,
    size: str = None,
):
    base_query = """
            SELECT ?book_id
                    WHERE {
                            [QUERY_INFO]
                            OPTIONAL {?book :hasID ?book_id} .
                            }
        """
    query_info = ""
    if category:
        query_info += f"?book rdf:type :{category} ."
    if title:
        query_info += f'?book :hasTitle "{title}" .'
    if author:
        query_info += f'?author :authorHasName "{author}" . ?author :isAuthorOf ?book .'
    if publisher:
        query_info += f'?publisher :publisherHasName "{publisher}" . ?publisher :isPublisherOf ?book .'
    if year:
        query_info += f"?book :hasPublishYear {year} ."
    if page:
        page_min, page_max = int(page) - 50, int(page) + 50
        query_info += f"?book :hasNumberPage ?page . FILTER (?page > {page_min}) . FILTER (?page < {page_max})"
    if language:
        query_info += (
            f'?language :languageHasName "{language}" . ?book :hasLanguage ?language .'
        )
    if extension:
        query_info += f'?book :hasExtension "{extension}" .'
    if rate:
        rate_min, rate_max = float(rate) - 0.3, float(rate) + 0.3
        query_info += f"?book :hasRate ?rate . FILTER (?page > {rate_min}) . FILTER (?page < {rate_max})"
    if size:
        query_info += f"?book :hasSize {size} ."

    if not query_info:
        query = """
            SELECT ?book_id
                WHERE {
                    ?book rdf:type ?childClass .
                    ?childClass rdfs:subClassOf* :Book .
                    OPTIONAL {?book :hasID ?book_id} .
                }
        """
    else:
        query = base_query.replace("[QUERY_INFO]", query_info)
    return query


def search_book(
    category: str = None,
    title: str = None,
    author: str = None,
    publisher: str = None,
    year: int = None,
    page: int = None,
    language: str = None,
    extension: str = None,
    rate: float = None,
    size: str = None,
):
    query = search_book_query(
        category, title, author, publisher, year, page, language, extension, rate, size
    )
    book_ids = list(default_world.sparql(base_query + query))
    book_ids = list(set([x[0] for x in book_ids]))
    books_info = []
    for book_id in book_ids[:25]:
        book_query = get_book_by_id_query(id=str(book_id))
        info = list(default_world.sparql(base_query + book_query))
        book_info = {
            "ID": info[0][0],
            "Author": [info[i][1] for i in range(len(info))],
            "Title": info[0][2],
            "Description": info[0][3],
            "Publisher": info[0][4],
            "Publish Year": info[0][5],
            "Number Pages": info[0][6],
            "Language": info[0][7],
        }
        books_info.append(book_info)
    return books_info
