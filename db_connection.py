# This file is responsible for creating weaviate client
import weaviate


class DbClient:
    instance = None
    connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(DbClient, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not self.connection:
            try:
                self.connection = weaviate.Client(
                    url="https://armorblox-weactivate-yj3agksl.weaviate.network",  # Replace with your endpoint
                    auth_client_secret=weaviate.AuthApiKey(api_key="ZlIfiiMFXAeKha1mk4VA6sBrOd3yMwe94EQL"), # Replace w/ your Weaviate instance API key
                    # additional_headers={
                    #     "X-HuggingFace-Api-Key": "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"  # Replace with your inference API key
                    # }
                )
                print("database connection established")
            except Exception as ex:
                print("failed to create db connection with error : {}".format(ex))