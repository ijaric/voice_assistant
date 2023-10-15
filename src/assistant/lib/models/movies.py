import datetime
import uuid

import pydantic


class Movie(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    rating: float | None = None
    type: str | None = None
    created: datetime.datetime
    modified: datetime.datetime
    creation_date: datetime.datetime | None = None
    runtime: int | None = None
    budget: int | None = None
    imdb_id: str | None = None

    @pydantic.computed_field
    @property
    def imdb_url(self) -> str:
        return f"https://www.imdb.com/title/{self.imdb_id}"

    def get_movie_info_line(self):
        not_provided_value = "not provided"
        content_film_info = {
            "Title": self.title,
            "Description": self.description or not_provided_value,
            "Rating": self.rating or not_provided_value,
            "Imdb_id": self.imdb_url or not_provided_value,
            "Creation_date": self.creation_date or not_provided_value,
            "Runtime": self.runtime or not_provided_value,
            "Budget": self.budget or not_provided_value,
        }
        content_film_info_line = ", ".join(f"{k}: {v}" for k, v in content_film_info.items())
        return content_film_info_line
