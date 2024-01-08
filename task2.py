from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from prettytable import PrettyTable

from models import Publisher, Sale, Book, Stock

SQLsystem = 'postgresql'
login = 'postgres'
password = 'postgres'
host = '192.168.0.5'
port = 5432
db_name = 'book_orm'
DSN = f'{SQLsystem}://{login}:{password}@{host}/{db_name}'

engine = create_engine(DSN)
session = Session(bind=engine)

def get_shops(s, publisher_input):
    my_table = PrettyTable()
    try:
        publisher_id = int(publisher_input)
        publisher = (s.query(Publisher).filter(Publisher.id == publisher_id).first())
    except ValueError:
        publisher = (s.query(Publisher).filter(Publisher.name == publisher_input).first())
    
    if publisher is None:
        print("Данный издатель не найден")
    else:
        sales = (
            session
            .query(Sale)
            .join(Stock)
            .join(Stock.shop) 
            .join(Book)
            .join(Publisher)
            .filter(Publisher.id == publisher.id)
            .order_by(Sale.date_sale)
            .all()
        )
        
        my_table.field_names = ["Название книги", "Название магазина", "Стоимость покупки", "Дата покупки"]
        for sale in sales:
            my_table.add_row([sale.stock3.book2.title, sale.stock3.shop.name, sale.price, sale.date_sale])
        print(my_table)
        print(f"Найдено {len(sales)} продаж для издателя {publisher.name}")

if __name__ == "__main__":
    publisher_input = input("Введите имя или идентификатор издателя: ")
    get_shops(session, publisher_input)
    

session.close()
