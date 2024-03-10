"""Q.
"""
import peewee
from database_manager import DatabaseManager
import local_settings

database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    user=local_settings.DATABASE['user'],
    password=local_settings.DATABASE['password'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)


class Transaction(peewee.Model):
    customer_code = peewee.CharField(
        max_length=255,
        null=False,
        verbose_name='Customer Code'
    )
    product_name = peewee.CharField(
        max_length=255,
        null=False,
        verbose_name='Product Name',
    )
    month = peewee.IntegerField(
        verbose_name='Month',
    )
    base_prices = peewee.FloatField(
        verbose_name='Base Price'
    )
    count = peewee.IntegerField(
        verbose_name='Count'
    )

    class Meta:
        database = database_manager.db


def initialize_database():
    try:
        print("start initializing database")
        database_manager.create_tables(models=[Transaction])
        with open("Transactions.csv", "r") as init:
            for i, line in enumerate(init):
                # We don't want to add first line.
                if i == 0:
                    continue
                trans = line.split(",")
                Transaction.create(
                    customer_code=trans[0],
                    product_name=trans[1],
                    month=trans[2],
                    base_prices=trans[3],
                    count=trans[4],
                )
    except Exception as e:
        print("Error", e)
    else:
        print("Database initialized")
    finally:
        # closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")


# def search_contact(search_term: str):
#     try:
#         retrieved_data = Contact.select().where(
#             (Contact.first_name.contains(search_term))
#             | (Contact.last_name.contains(search_term))
#             | (Contact.number.contains(search_term))
#             | (Contact.address.contains(search_term))
#         )
#         for contact in retrieved_data:
#             yield {
#                 "First Name": contact.first_name,
#                 "Last Name": contact.last_name,
#                 "Number": contact.number,
#                 "Address": contact.address,
#                 "Id": str(contact.get_id()),
#             }
#     except Exception as e:
#         print("Error", e)
#     finally:
#         # closing database connection.
#         if database_manager.db:
#             database_manager.db.close()
#             print("Database connection is closed")


# initialize database
# # Attention: after first start set local_settings.first_init to False
if local_settings.first_init:
    initialize_database()
