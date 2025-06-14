import sqlite3
from pathlib import Path
from typing import List
from pydantic import BaseModel
from loguru import logger
import pprint


class MediaItem(BaseModel):
    id: int
    url: str
    title: str
    description: str
    tags: List[str]


class VideoLinks(BaseModel):
    id: int 
    url: str
    title: str
    description: str
    tags: List[str]


class Resources(BaseModel):
    id: int
    url: str
    title: str
    description: str
    topic_tags: List[str]
    type: str


class DatabaseConnection:
    def __init__(self, media_db_path, links_db_path):
        self._media_connection = sqlite3.connect(str(media_db_path))
        self._links_connection = sqlite3.connect(str(links_db_path))

        for conn in (self._media_connection, self._links_connection):
            conn.row_factory = sqlite3.Row

    def close(self):
        self._media_connection.close()
        self._links_connection.close()

    # TODO dynamic improvement 
    def get_all_media(self) -> List[MediaItem]:
        """
        Fetch every record from the `images` table.
        """
        images_and_videos = {'images': None, 'videos': None}

        # IMAGES
        sql = "SELECT id, url, title, description, tags FROM images"
        rows = self._media_connection.execute(sql).fetchall()
        images_and_videos['images'] = [
            MediaItem(
                id=row["id"],
                url=row["url"],
                title=row["title"],
                description=row["description"],
                tags=(row["tags"].split(',')),
            )
            for row in rows
        ]

        # VIDEOS
        sql = "SELECT id, url, title, description, tags FROM videos"
        rows = self._media_connection.execute(sql).fetchall()
        images_and_videos['videos'] = [
            MediaItem(
                id=row["id"],
                url=row["url"],
                title=row["title"],
                description=row["description"],
                tags=(row["tags"].split(',')),
            )
            for row in rows
        ]

        return images_and_videos

    def get_all_resources(self) -> List[Resources]:
        """
        Fetch every resource from the 'resources' table
        """
        sql = "SELECT id, url, title, description, topic_tags, type FROM resources"
        rows = self._links_connection.execute(sql).fetchall()
        return [
            Resources(
                id=row["id"],
                url=row["url"],
                title=row["title"],
                description=row["description"],
                topic_tags=(row["topic_tags"].split(',')),
                type=(row['type'])
            )
            for row in rows
        ]


if __name__ == "__main__":
    # Example usage 
    links_db_path  = '/Users/michaelfedotov/Downloads/ai_takehome/links.db'
    media_db_path = '/Users/michaelfedotov/Downloads/ai_takehome/media.db'
    db = DatabaseConnection(media_db_path, links_db_path)


    all_media = db.get_all_media()    
    all_links = db.get_all_resources()    
    db.close()

    # pprint.pprint(all_media['images'])
    pprint.pprint(all_media['videos'])
    # pprint.pprint(all_links)
