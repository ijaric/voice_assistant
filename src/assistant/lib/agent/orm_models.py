import datetime
import uuid

import pgvector.sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import sqlalchemy.sql as sa_sql

import lib.models.orm as base_models


class Genre(base_models.Base):
    __tablename__: str = "genre"

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
    __tablename__: str = "person"

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: sa_orm.Mapped[str] = sa_orm.mapped_column()
    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now()
    )
    modified: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )


class FilmWork(base_models.Base):
    __tablename__: str = "film_work"

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)
    title: sa_orm.Mapped[str]
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    creation_date: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(nullable=True)
    file_path: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    rating: sa_orm.Mapped[float] = sa_orm.mapped_column(nullable=True)
    type: sa_orm.Mapped[str] = sa_orm.mapped_column()
    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now()
    )
    modified: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )
    embedding: sa_orm.Mapped[list[float]] = sa_orm.mapped_column(pgvector.sqlalchemy.Vector(1536))
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


class ChatHistory(base_models.Base):
    __tablename__: str = "chat_history"

    id: sa_orm.Mapped[uuid.UUID] = sa_orm.mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: sa_orm.Mapped[str] = sa_orm.mapped_column()
    channel: sa_orm.Mapped[str] = sa_orm.mapped_column()
    user_id: sa_orm.Mapped[str] = sa_orm.mapped_column()
    content: sa_orm.Mapped[sa.JSON] = sa_orm.mapped_column(sa.JSON)
    created: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now()
    )
    modified: sa_orm.Mapped[datetime.datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True), server_default=sa_sql.func.now(), onupdate=sa_sql.func.now()
    )
