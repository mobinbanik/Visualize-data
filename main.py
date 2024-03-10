"""Visualize data."""
import matplotlib.pyplot as plt
import database
# import pandas as pd


def has_multiple_customer(customers: list[dict]) -> bool:
    flag_multiple_customer = False
    first_customer = customers[0]["customer_code"]
    for customer in customers:
        if customer["customer_code"] != first_customer:
            flag_multiple_customer = True
            break
    return flag_multiple_customer


def remove_customers(customers: list[dict], customer_code: str):
    print(customers)
    print(f"we found more than one customer code <{customer_code}>.")
    print("\nEnter customer code you want in this list")
    customer_code = input(
        "Enter your customer code:(example:'Z-534', 'V-718', 'L-302')\n"
    ).lower()
    selected_customer = list()
    for i, customer in enumerate(customers):
        if customer_code in customer["customer_code"].lower():
            selected_customer.append(customer)

    if has_multiple_customer(selected_customer):
        return remove_customers(selected_customer, customer_code)
    else:
        return selected_customer


def get_customer_from_database():
    customer_code = input(
        "Enter your customer code:(example:'Z-534', 'V-718', 'L-302')\n"
    )
    selected_customer = list(database.get_customer_by_code(customer_code))
    if len(selected_customer) == 0:
        print(f"No customer with this code: '{customer_code}' found.")
        # Do you want to continue?
        print("if you want to check another customer code enter 'y'")
        print("if you want exit enter any key")
        flag = input("do you want to continue? (y):").lower()
        if flag == "y":
            # Restart
            return get_customer_from_database()
        else:
            # Exit
            exit()

    if has_multiple_customer(selected_customer):
        selected_customer = remove_customers(selected_customer, customer_code)
    return selected_customer


def main():
    """Main function."""
    try:
        # Select 1 customer
        selected_customer = get_customer_from_database()
        customer_code = selected_customer[0]["customer_code"]
        # Sort by month
        sorted_customer = sorted(selected_customer, key=lambda x: x['month'])
        print(sorted_customer)

        # Initialize lists and dict
        month_number_of_sold_product = list()
        month_total_profit = list()
        dict_number_of_purchases_each_product = dict()
        dict_amount_of_purchases_each_product = dict()
        for i in range(12):
            month_number_of_sold_product.append(0)
            month_total_profit.append(0.0)

        # Fill list and dict
        for record in sorted_customer:
            # List
            #   Add count to list with month index
            month_number_of_sold_product[record["month"] - 1] \
                += record["count"]
            #   Add total price to list with month index
            month_total_profit[record["month"] - 1] \
                += record["count"] * record["base_price"]

            # Dict
            #   Add each product was bought to dict
            #       If product not in dict: add to dict
            if record["product_name"] not in dict_number_of_purchases_each_product:
                dict_number_of_purchases_each_product[record["product_name"]] \
                    = record["count"]
                dict_amount_of_purchases_each_product[record["product_name"]] \
                    = int(record["count"] * record["base_price"])
            #       if product in dict: Update the previous one
            else:
                dict_number_of_purchases_each_product[record["product_name"]] \
                    += record["count"]
                dict_amount_of_purchases_each_product[record["product_name"]] \
                    += int(record["count"] * record["base_price"])

        # Print our extracted data
        print("month: number of sold:", month_number_of_sold_product)
        print("month: amount of sold:", month_total_profit)
        print("products/number:", dict_number_of_purchases_each_product)
        print("products/amount:", dict_amount_of_purchases_each_product)

        # Create chart 1 and show
        plt.bar(range(1, 13), month_number_of_sold_product)
        plt.xlabel("Month")
        plt.ylabel("Count")
        plt.title(f"The number of purchases made by customer {customer_code}")
        plt.show()

        # Create chart 2 and show
        plt.bar(range(1, 13), month_total_profit)
        plt.xlabel("Month")
        plt.ylabel("profit($)")
        plt.title(f"Purchase amount by customer {customer_code}")
        plt.show()

        # Extract keys and values from dict to list
        list_keys_of_purchases_dict = list(dict_number_of_purchases_each_product.keys())
        list_values_of_purchases_dict = list(dict_number_of_purchases_each_product.values())
        list_keys_of_amount_of_purchases_dict = list(dict_amount_of_purchases_each_product.keys())
        list_values_of_amount_of_purchases_dict = list(dict_amount_of_purchases_each_product.values())

        # Create chart 3 and show
        fig, ax = plt.subplots()
        plt.bar(list_keys_of_purchases_dict, list_values_of_purchases_dict)

        # Set rotation and size for label
        ax.xaxis.set_tick_params(rotation=15, labelsize=8)
        plt.xlabel("Products")
        plt.ylabel("Number of Purchases")
        plt.title(f"Products purchased by the customer {customer_code}")
        plt.show()

        # Create chart 4 and show
        plt.pie(
            list_values_of_amount_of_purchases_dict,
            labels=list_values_of_amount_of_purchases_dict,
            startangle=90,
            shadow=True
        )

        # Create a legend
        plt.legend(list_keys_of_amount_of_purchases_dict)
        plt.title(f"Pie Chart Amount of Purchases ($)")
        plt.show()
    except NameError as e:
        print("%s" % e)
    else:
        print("Done!!!")


if __name__ == '__main__':
    main()
