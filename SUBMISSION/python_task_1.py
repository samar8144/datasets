import pandas as pd
import numpy as np


def generate_car_matrix(df):
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    # pivote the data frame to create a matrix
    car_matrix = df.pivot(index="id_1",columns="id_2",values="car")
    # Fill NaN value with 0
    car_matrix = car_matrix.fillna(0)
    # Set digonal value to 0
    for col in car_matrix.columns:
        car_matrix.loc[col,col] = 0

    return car_matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    cond = [(df["car"]<=15),
            (df["car"]>15) & (df["car"]<=25),
            (df["car"] >25)]
    choi = ["low","medium","high"]
    df["car_type"] = pd.Series(np.select(cond,choi),dtype="category")
    type_count = df["car_type"].value_counts().to_dict()
    sorted_type_count = dict(sorted(type_count.items()))

    return sorted_type_count


def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_index = df[df["bus"]>2*df["bus"].mean()].index.to_list()
    bus_index.sort()

    return bus_index


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    rout_avg_truck = df.groupby("route")["truck"].mean()
    filterd_rout = rout_avg_truck[rout_avg_truck > 7].index.to_list()
    filterd_rout.sort()

    return filterd_rout


def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    mod_matrix = matrix.applymap(lambda x: x*0.75 if x > 20 else x* 1.25)
    mod_matrix = matrix.round(1)

    return matrix


def time_check(df):
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['duration'] = df['end_datetime'] - df['start_datetime']
    completeness_check = (
        (df['duration'] == pd.Timedelta(days=1)) &  
        (df['start_datetime'].dt.dayofweek == 0) &  
        (df['end_datetime'].dt.dayofweek == 6)  
    )
    result_series = completeness_check.groupby(['id', 'id_2']).all()
    
    return result_series
