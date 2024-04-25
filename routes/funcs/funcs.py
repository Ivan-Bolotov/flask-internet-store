from data.db_session import create_session, global_init
from data.products import Product
from data.users import User


# Подключение к БД, если его не было
global_init("db/main_db.db")


def get_amount_of_users() -> int:
    db_session = create_session()
    return len(db_session.query(User).all())


def get_amount_of_products() -> int:
    db_session = create_session()
    return len(db_session.query(Product).all())
