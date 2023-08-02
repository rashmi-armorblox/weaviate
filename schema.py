# This file is responsible for schema related details
import json

import requests

from db_connection import DbClient

client = DbClient().connection


def create_schema():
    class_obj = {
        'class': 'Questionnaire',
        'properties': [
            {
                'name': 'question',
                'dataType': ['text'],
            },
            {
                'name': 'answer',
                'dataType': ['text'],
            },
            {
                'name': 'category',
                'dataType': ['text'],
            },
        ],
        "vectorizer": "text2vec-huggingface",
        # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        "moduleConfig": {
            "text2vec-huggingface": {
                "model": "sentence-transformers/all-MiniLM-L6-v2",  # Can be any public or private Hugging Face model.
                "options": {
                    "waitForModel": True
                }
            }
        }
    }
    client.schema.create_class(class_obj)


def get_schema(class_name: str):
    if class_name is None:
        schemas = client.schema.get()
        print(schemas)
    else:
        schema = client.schema.get(class_name)
        print(schema)


def update_schema():
    changed_class_obj = {
        "class": "Questionnaire",
        "vectorIndexConfig": {
            "distance": "dot"  # Change the distance metric
        }
    }
    client.schema.update_config("Questionnaire", changed_class_obj)


def delete_schema():
    client.schema.delete_class("Questionnaire")


# add property to existing schema
def add_property_to_schema():
    add_prop = {
        'name': 'category',
        'dataType': ['text'],
    }
    client.schema.property.create('Question', add_prop)


def import_data():
    url = 'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json'
    resp = requests.get(url)
    data = json.loads(resp.text)

    # Configure a batch process
    with client.batch(
            batch_size=100
    ) as batch:
        # Batch import all Questions
        for i, d in enumerate(data):
            print(f"importing question: {i + 1}")

            properties = {
                "answer": d["Answer"],
                "question": d["Question"],
                "category": d["Category"],
            }

            client.batch.add_data_object(
                properties,
                "Questionnaire",
            )


def delete_object():
    result = (
        client.batch.delete_objects(
            class_name='Questionnaire',
            # Same `where` filter as in the GraphQL API
            where={
                'path': ['answer'],
                'operator': 'Equal',
                'valueText': 'liver'
            },
            dry_run=True,
            output='verbose'
        )
    )

    import json
    print(json.dumps(result, indent=2))


# create_schema()
# get_schema("Questionnaire")
import_data()