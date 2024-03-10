"""Visualize data."""
import matplotlib.pyplot as plt
# import pandas as pd


# def search_string(s, search: str) -> bool:
#     """Search string.
#
#     :param s: data
#     :param search: string you want to search.
#     :return: True or False. <search> is in <s> or not.
#     """
#     return search in str(s).lower()
#
#
# def filter_data_frame(string: str, data: pd.DataFrame) -> pd.DataFrame:
#     """Filter data frame with given string.
#
#     :param string: string to filter
#     :param data: data frame to filter
#     :return: pd.DataFrame with filtered data
#     """
#     # Search for the string in all columns
#     # Data.apply(lambda x:...): apply a function to each row of data frame
#     # Pd.series.map(lambda s:...): apply a function to each member of row
#     # So create a true false Dataframe based on given name
#     mask = data.apply(lambda x: x.map(lambda s: search_string(s, string)))
#     # Filter the DataFrame based on the mask
#     # Mask.any(axis=1): return row that contains True cells.
#     # Axis=1 for return row contains True
#     # Axis=0 for return column contains True
#     # Axis=None reduce in all axis
#     filtered_df = data.loc[mask.any(axis=1)]
#     return filtered_df
#
#
# def return_customer_df_selected_by_input(
#         data: pd.DataFrame,
#         code: str
# ) -> pd.DataFrame:
#     """Return customer selection by user input.
#
#     Get code of customer and check it in data frame.
#     if noting found ask user for retry or end for operation.
#     if more than 1 customer found, ask user to select one customer among them
#     finally return 1 selected customer.
#     :param data: data frame to check.
#     :param code: code of customer to select from data frame
#     :return: pd.Dataframe return 1 product with from data.
#     """
#     filtered_df = filter_data_frame(code, data[["Customer Code"]])
#     # If <name> not exist
#     if filtered_df.empty:
#         # Warning: name not found
#         print(f"No customer with this code: '{code}' found.")
#         # Do you want to continue?
#         print("if you want to check another customer code enter 'y'")
#         print("if you want exit enter any key")
#         flag = input("do you want to continue? (y):").lower()
#         if flag == "y":
#             # Restart
#             return None
#         else:
#             # Exit
#             exit()
#     # If more than 1 product found
#     elif len(filtered_df.drop_duplicates(subset="Customer Code")) >= 2:
#         print(f"we found more than one customer code <{code}>.")
#         print(filtered_df)
#         print("\nEnter customer code you want in this list")
#         customer_code = input(
#             "Enter your customer code:(example:'Z-534', 'V-718', 'L-302')\n"
#         ).lower()
#         return return_customer_df_selected_by_input(filtered_df, customer_code)
#     # If just 1 product found
#     elif len(filtered_df.drop_duplicates(subset="Customer Code")) == 1:
#         return filtered_df


def main():
    """Main function."""
    try:
        # Read data
        data = pd.read_csv("Transactions.csv")
        # Remove transactions that total cost is 0
        # Remove wrong row
        # Dataframe.Itertuples(): Iterate over DataFrame rows as named tuples.
        # Output(row) =
        # Pandas(
        #   Index=186,
        #   _1='Z-534',
        #   _2='Lenovo-181',
        #   Month=11,
        #   _4=1032.59,
        #   Count=12,
        #   _6=12391.08,
        # )
        for row in data.itertuples():
            # Row._6 is Total Price
            # If total price is 0 remove that row
            if row._6 == 0:
                data.drop(index=row.Index, inplace=True)
        # Select 1 product
        customer_code = str()
        selected_customer = None
        while selected_customer is None:
            customer_code = input(
                "Enter your customer code:(example:'Z-534', 'V-718', 'L-302')\n"
            ).lower()
            selected_customer = return_customer_df_selected_by_input(
                data,
                customer_code
            )
        # Left join: data join to selected customer
        selected_customer = data.merge(
            selected_customer,
            on="Customer Code",
            how="right"
        )
        # Sort by month
        sorted_customer = selected_customer.sort_values(by=['Month'])
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
        # Dataframe.Itertuples(): Iterate over DataFrame rows as named tuples.
        # Output(row) =
        # Pandas(
        #   Index=186,
        #   _1='Z-534',
        #   _2='Lenovo-181',
        #   Month=11,
        #   _4=1032.59,
        #   Count=12,
        #   _6=12391.08,
        # )
        for row in sorted_customer.itertuples():
            # Add count to list with row.Month index
            month_number_of_sold_product[row.Month - 1] += row.Count
            # Add total price to list with row.Month index
            month_total_profit[row.Month - 1] += row._6
            # Add each product was bought to dict
            # If product not in dict: add to dict
            if row._2 not in dict_number_of_purchases_each_product:
                dict_number_of_purchases_each_product[row._2] = row.Count
                dict_amount_of_purchases_each_product[row._2] = int(row._6)
            # if product in dict: Update the previous one
            else:
                dict_number_of_purchases_each_product[row._2] += row.Count
                dict_amount_of_purchases_each_product[row._2] += int(row._6)
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
