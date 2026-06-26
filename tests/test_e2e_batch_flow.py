from lib.techladder_client import TechladderClient


def test_e2e_batch_flow():
    client = TechladderClient()

    # Step 1: Authentication
    client.authenticate()

    # Step 2: Create Batch
    batch_id = client.create_batch()

    # Step 3: Get Batch
    client.get_batch(batch_id)

    # Step 4: Poll Results
    assert client.poll_results(batch_id)