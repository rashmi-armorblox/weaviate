# This file consists of search queries
import json

from db_connection import DbClient


# semantic_search : search from Questionnaire class with `nearText` and limit response size to 2
def semantic_search():
    nearText = {"concepts": ["biology"]}
    response = (
    DbClient().connection.query
    .get("Questionnaire", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
    )
    print(json.dumps(response, indent=4))


# semantic_search_with_filter: search from Questionnaire class with `nearText`, where clause and limit response size to 2
def semantic_search_with_filter():
    nearText = {"concepts": ["biology"]}

    response = (
        DbClient().connection.query
            .get("Questionnaire", ["question", "answer", "category"])
            .with_near_text(nearText)
            .with_where({
            "path": ["category"],
            "operator": "Equal",
            "valueText": "ANIMALS"
        }).with_limit(2).do()
    )
    print(json.dumps(response, indent=4))


semantic_search()
# semantic_search_with_filter()