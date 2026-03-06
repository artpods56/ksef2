from ksef2 import Client, Environment


client = Client(environment=Environment.TEST)


for provider in client.peppol.all():
    print(provider.model_dump_json(indent=2))
