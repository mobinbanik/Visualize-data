"""Database modules."""
import peewee
from database_manager import DatabaseManager
import local_settings

# Database instance
database_manager = DatabaseManager(
    database_name=local_settings.DATABASE['name'],
    user=local_settings.DATABASE['user'],
    password=local_settings.DATABASE['password'],
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
)


class Transaction(peewee.Model):
    """Transaction model."""
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
    base_price = peewee.FloatField(
        verbose_name='Base Price'
    )
    count = peewee.IntegerField(
        verbose_name='Count'
    )

    class Meta:
        """Meta class."""
        database = database_manager.db


def initialize_database():
    """Initialize database.

    Create tables if they don't exist and fill with initial values.
    if you don't want to initialize the database:
    set sample_settings.first_init to False.
    """
    try:
        # Warning
        print("start initializing database")
        # # you can uncomment these statements For more caution.
        # print("do you want to continue? [y/n]")
        # if input().lower() not in ['y', 'yes']:
        #     exit()

        # Create table
        database_manager.create_tables(models=[Transaction])
        with open("Transactions.csv", "r") as init:
            # Get transactions line by line
            for i, line in enumerate(init):
                # We don't want to add first line.
                if i == 0:
                    continue
                trans = line.split(",")
                Transaction.create(
                    customer_code=trans[0],
                    product_name=trans[1],
                    month=trans[2],
                    base_price=trans[3],
                    count=trans[4],
                )
    except Exception as e:
        print("Error", e)
    else:
        print("Database initialized")
    finally:
        # Closing database connection
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")


def get_customer_by_code(search_term: str):
    """Get customer by code.

    :param search_term: search term
    :return: retrieved data
    """
    try:
        print("start getting customers by code")
        # Query
        retrieved_data = Transaction.select().where(
            (Transaction.customer_code.contains(search_term))
            & (Transaction.count != 0)
        )
        for trans in retrieved_data:
            yield {
                "customer_code": trans.customer_code,
                "product_name": trans.product_name,
                "month": trans.month,
                "base_price": trans.base_price,
                "count": trans.count,
            }
    except Exception as e:
        print("Error", e)
    finally:
        # closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")


# initialize database
# Attention: after first start set local_settings.first_init to False
if local_settings.first_init:
    initialize_database()
