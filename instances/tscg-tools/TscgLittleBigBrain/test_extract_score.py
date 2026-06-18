from tests.test_api_client import TscgAPIClient
client = TscgAPIClient()
poclets = client.get_poclets_with_scores()
for p in poclets[:3]:
    print(p)