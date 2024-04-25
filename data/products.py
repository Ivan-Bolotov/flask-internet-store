import sqlalchemy
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = "Products"

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    image = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tag = sqlalchemy.Column(sqlalchemy.String, nullable=False)
