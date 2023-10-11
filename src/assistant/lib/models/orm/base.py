import datetime
import uuid

import pgvector.sqlalchemy  # type: ignore[reportMissingImports]
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import sqlalchemy.sql as sa_sql


class TimestampMixin:
    """Mixin with timestamp fields."""

    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(server_default=sa_sql.func.now())
    modified: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )


class IdMixin:
    """Mixin with UUID id field."""

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)


class Base(sa_orm.DeclarativeBase):
    """Base class for all models."""

    __mapper_args__ = {"eager_defaults": True}
    __table_args__ = {"schema": "content"}


class GenreFilmWork(Base):
    __tablename__: str = "genre_film_work"

    genre_id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(sa.ForeignKey("content.genre.id"), primary_key=True)
    film_work_id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(
        sa.ForeignKey("content.film_work.id"), primary_key=True
    )

    genre = sa_orm.relationship("Genre", back_populates="film_works")
    film_work = sa_orm.relationship("FilmWork", back_populates="genres")


class PersonFilmWork(Base):
    __tablename__: str = "person_film_work"

    person_id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(sa.ForeignKey("content.person.id"), primary_key=True)
    film_work_id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(
        sa.ForeignKey("content.film_work.id"), primary_key=True
    )
    role: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=False)

    person = sa_orm.relationship("Person", back_populates="film_works")
    film_work = sa_orm.relationship("FilmWork", back_populates="persons")


class Genre(Base, IdMixin, TimestampMixin):
    __tablename__: str = "genre"

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=False)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column()
    film_works = sa_orm.relationship("GenreFilmWork", back_populates="genre")


class Person(Base, IdMixin, TimestampMixin):
    __tablename__: str = "person"

    full_name: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=False)
    film_works = sa_orm.relationship("PersonFilmWork", back_populates="person")


class FilmWork(Base, IdMixin, TimestampMixin):
    __tablename__: str = "film_work"

    title: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=False)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column()
    creation_date: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column()
    rating: sa_orm.Mapped[float] = sa_orm.mapped_column(nullable=False)
    type: sa_orm.Mapped[str] = sa_orm.mapped_column()
    runtime: sa_orm.Mapped[int] = sa_orm.mapped_column(nullable=False)
    adult: sa_orm.Mapped[bool] = sa_orm.mapped_column(default=False)
    budget: sa_orm.Mapped[int] = sa_orm.mapped_column(default=0)
    imdb_id: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=False)
    original_language: sa_orm.Mapped[str] = sa_orm.mapped_column()
    revenue: sa_orm.Mapped[int] = sa_orm.mapped_column()
    vote_count: sa_orm.Mapped[int] = sa_orm.mapped_column()
    embeddings: sa_orm.Mapped[  # type: ignore[reportUnknownVariableType]
        pgvector.sqlalchemy.Vector
    ] = sa_orm.mapped_column(
        pgvector.sqlalchemy.Vector(1536)  # type: ignore[reportUnknownArgumentType]
    )
    genres = sa_orm.relationship("GenreFilmWork", back_populates="film_work")
    persons = sa_orm.relationship("PersonFilmWork", back_populates="film_work")
