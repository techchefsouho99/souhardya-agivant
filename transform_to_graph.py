# transform_to_graph.py

def map_user_vertices(users_df):
    return users_df.select(
        "user_id",
        "username",
        "email",
        "created_at"
    )


def map_product_vertices(products_df):
    return products_df.select(
        "product_id",
        "category",
        "price",
        "created_at"
    )


def map_purchased_edges(transactions_df):
    return transactions_df.select(
        "txn_id",
        "user_id",
        "product_id",
        "amount",
        "timestamp"
    )
