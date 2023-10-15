import datetime
import uuid

import pgvector.sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import sqlalchemy.sql as sa_sql

import lib.orm_models.base as base_models


class Genre(base_models.Base):
    __tablename__: str = "genre"  # type: ignore[reportIncompatibleVariableOverride]

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)
    name: sa_orm.Mapped[str] = sa_orm.mapped_column()
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now()
    )
    modified: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )


class Person(base_models.Base):
    __tablename__: str = "person"  # type: ignore[reportIncompatibleVariableOverride]

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: sa_orm.Mapped[str] = sa_orm.mapped_column()
    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now()
    )
    modified: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )


class FilmWork(base_models.Base):
    __tablename__: str = "film_work"  # type: ignore[reportIncompatibleVariableOverride]

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)
    title: sa_orm.Mapped[str] = sa_orm.mapped_column()
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    creation_date: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(nullable=True)
    rating: sa_orm.Mapped[float] = sa_orm.mapped_column(nullable=True)
    runtime: sa_orm.Mapped[int] = sa_orm.mapped_column(nullable=False)
    budget: sa_orm.Mapped[int] = sa_orm.mapped_column(default=0)
    imdb_id: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=False)
    type: sa_orm.Mapped[str] = sa_orm.mapped_column()
    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now()
    )
    modified: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )
    embeddings: sa_orm.Mapped[list[float]] = sa_orm.mapped_column(pgvector.sqlalchemy.Vector(1536))
    genres: sa_orm.Mapped[list[Genre]] = sa_orm.relationship(secondary="genre_film_work")


GenreFilmWork = sa.Table(
    "genre_film_work",
    base_models.Base.metadata,
    sa.Column("id", sa.UUID, primary_key=True),  # type: ignore[reportUnknownVariableType]
    sa.Column("genre_id", sa.ForeignKey(Genre.id), primary_key=True),  # type: ignore[reportUnknownVariableType]
    sa.Column("film_work_id", sa.ForeignKey(FilmWork.id), primary_key=True),  # type: ignore[reportUnknownVariableType]
    sa.Column("created", sa.DateTime(timezone=True), server_default=sa_sql.func.now()),
)


PersonFilmWork = sa.Table(
    "person_film_work",
    base_models.Base.metadata,
    sa.Column("person_id", sa.ForeignKey(Person.id), primary_key=True),  # type: ignore[reportUnknownVariableType]
    sa.Column("film_work_id", sa.ForeignKey(FilmWork.id), primary_key=True),  # type: ignore[reportUnknownVariableType]
    sa.Column("role", sa.String(50), nullable=False),
    sa.Column("created", sa.DateTime(timezone=True), server_default=sa_sql.func.now()),
)
