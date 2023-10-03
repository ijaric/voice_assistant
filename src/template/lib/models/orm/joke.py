import sqlalchemy.orm as sa_orm

import lib.models.orm.base as base

Base = base.Base


class JokeORM(Base):
    __tablename__ = "joke"  # type: ignore

    type_field: sa_orm.Mapped[str] = sa_orm.mapped_column(name="type", nullable=False)
    setup: sa_orm.Mapped[str] = sa_orm.mapped_column()
    punchline: sa_orm.Mapped[str] = sa_orm.mapped_column()
