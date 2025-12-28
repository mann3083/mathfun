import os
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

ENDPOINT = os.getenv("COSMOS_ENDPOINT")
KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = "MathMasterDB"
CONTAINER_NAME = "QuizResults"

class CosmosDBManager:
    def __init__(self):
        if not ENDPOINT or not KEY:
            raise ValueError("Missing Cosmos DB credentials in .env file")
        
        self.client = CosmosClient(ENDPOINT, KEY)
        self.database = self.client.create_database_if_not_exists(id=DATABASE_NAME)
        
        # Partition Key is critical for scaling. We use /user_id.
        self.container = self.database.create_container_if_not_exists(
            id=CONTAINER_NAME, 
            partition_key=PartitionKey(path="/user_id")
        )

    def save_submission(self, timestamp_key, submission_data):
        """
        Saves a quiz result to Cosmos DB.
        Structure: We flatten it slightly to make it a valid document.
        """
        document = {
            "id": timestamp_key,          # Unique ID for Cosmos
            "user_id": "guest",           # Placeholder for future multi-user support
            "timestamp_key": timestamp_key, 
            "summary": submission_data['summary'],
            "details": submission_data['details']
        }
        
        self.container.create_item(body=document)

    def get_all_history(self):
        """
        Fetches all history and transforms it back to the dictionary format 
        expected by the frontend: { "DD-MM-YY...": { "summary": ..., "details": ... } }
        """
        query = "SELECT * FROM c WHERE c.user_id = 'guest'"
        items = self.container.query_items(
            query=query,
            enable_cross_partition_query=True
        )

        # Transformation Layer (Cosmos List -> Frontend Dictionary)
        history_dict = {}
        for item in items:
            key = item['id']
            history_dict[key] = {
                "summary": item['summary'],
                "details": item['details']
            }
            
        return history_dict

# Singleton instance
db_manager = CosmosDBManager()