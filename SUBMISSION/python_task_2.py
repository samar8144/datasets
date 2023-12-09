import pandas as pd
from datetime import time


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix = pd.DataFrame(index=df["id_start"].unique(), columns=df['id_end'].unique(), dtype=float)
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0
    for index, row in df.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
        if not pd.isna(distance_matrix.at[id_start, id_end]) and not pd.isna(distance_matrix.at[id_end, id_start]):
            distance_matrix.at[id_start, id_end] += distance
            distance_matrix.at[id_end, id_start] += distance
        else:
            distance_matrix.at[id_start, id_end] = distance
            distance_matrix.at[id_end, id_start] = distance

    return distance_matrix


def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here 
    unrolled_data = []
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                distance = distance_matrix.at[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_df = df[df['id_start'] == reference_id]
    reference_avg_distance = reference_df['distance'].mean()
    threshold_range = 0.1 * reference_avg_distance
    filtered_ids = df[
        (df['id_start'] != reference_id) &
        (df['distance'] >= reference_avg_distance - threshold_range) &
        (df['distance'] <= reference_avg_distance + threshold_range)
    ]['id_start'].unique()
    filtered_ids.sort()

    return filtered_ids


def calculate_toll_rate(df):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)), (time(10, 0, 0), time(18, 0, 0)), (time(18, 0, 0), time(23, 59, 59))]
    weekend_time_range = (time(0, 0, 0), time(23, 59, 59))
    
    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7

    df['start_day'] = df['start_datetime'].dt.day_name()
    df['start_time'] = df['start_datetime'].dt.time
    df['end_day'] = df['end_datetime'].dt.day_name()
    df['end_time'] = df['end_datetime'].dt.time

    df['discount_factor'] = 1.0  # Default discount factor

    for i, (start_time, end_time) in enumerate(weekday_time_ranges):
        weekday_condition = (df['start_time'] >= start_time) & (df['start_time'] <= end_time) & (df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
        df.loc[weekday_condition, 'discount_factor'] = weekday_discount_factors[i]

    weekend_condition = df['start_day'].isin(['Saturday', 'Sunday'])
    df.loc[weekend_condition, 'discount_factor'] = weekend_discount_factor

    vehicle_columns = ['moto', 'car', 'rv', 'bus', 'truck']
    for column in vehicle_columns:
        df[column] *= df['discount_factor']

    df.drop(['start_day', 'start_time', 'end_day', 'end_time', 'discount_factor'], axis=1, inplace=True)

    return df
