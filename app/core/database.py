"""
Database connection and utilities.
"""

from pymongo import MongoClient
from pymongo.database import Database
from app.core.config import settings


class MongoDB:
    """
    MongoDB connection manager.
    """

    def __init__(self):
        self.client: MongoClient | None = None
        self.database: Database | None = None

    def connect(self):
        if self.database is not None:
            return  # Already connected

        try:
            self.client = MongoClient(settings.MONGODB_URL)
            self.database = self.client[settings.MONGODB_DB_NAME]
            self.client.admin.command("ping")

            print(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")

        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            raise

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.database = None
            print("👋 MongoDB connection closed")

    def get_database(self) -> Database:
        if self.database is None:
            self.connect()
        return self.database


# Global instance
mongodb = MongoDB()


def get_database() -> Database:
    """
    Safe database accessor.
    Auto-connects if needed.
    """
    return mongodb.get_database()
