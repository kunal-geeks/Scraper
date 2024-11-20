import pandas as pd
import re  # For regex operations


def preprocess_value(value, is_change_column=False):
    """
    Preprocess a value by:
    - Removing commas
    - Removing unwanted characters (letters and symbols)
    - Handling negative numbers and bond price formats
    - Converting to float
    :param value: The value to preprocess
    :param is_change_column: Whether the value belongs to the 'Change' column
    """
    if isinstance(value, str):
        # Remove commas
        value = value.replace(',', '')

        # Remove unwanted characters (letters and symbols)
        value = re.sub(r'[^0-9\.\-\+]', '', value)

        # Special handling for the 'Change' column
        if is_change_column:
            if value.startswith('-') and value.count('-') == 1:
                # If it starts with a single "-", treat it as a negative number
                return float(value)
            elif '-' in value:
                # Replace '-' in the middle with '.'
                parts = value.split('-')
                if len(parts) == 2:  # Cases like "-5-2" or "+6-2"
                    sign = "-" if value.startswith('-') else ""
                    value = sign + parts[0].replace('+', '') + '.' + parts[1] + '0' if len(parts[1]) == 1 else sign + parts[0].replace('+', '') + '.' + parts[1]
                else:
                    # Cases like "1001-4"
                    value = parts[0] + '.' + parts[1]
        else:
            # Replace '-' in the middle for non-'Change' columns
            value = value.replace('-', '.')

    # Convert to float if possible
    try:
        return float(value)
    except ValueError:
        return None  # Return None if conversion fails


def clean_and_add_mean(df):
    """
    Processes the dataframe:
    - Drops the 'Links' column
    - Cleans the 'Last', 'Change', 'High', and 'Low' columns
    - Computes the 'Mean' column
    - Finds the row with the largest 'Change'
    """

    # Drop the 'Links' column
    df = df.drop(columns=['Links'], axis=1)

    # Columns to clean
    columns_to_clean = ['Last', 'High', 'Low']

    # Clean the specified columns
    for column in columns_to_clean:
        df[column] = df[column].apply(preprocess_value)

    # Clean the 'Change' column with special rules
    df['Change'] = df['Change'].apply(lambda x: preprocess_value(x, is_change_column=True))

    # Calculate the 'Mean' column as the average of 'High' and 'Low'
    df['Mean'] = df[['High', 'Low']].mean(axis=1)

    # Find the row with the largest 'Change'
    max_change_row = df.loc[df['Change'].idxmax()]
    print(f"Contract with largest change: {max_change_row['Contract Name']} with Last Price: {max_change_row['Last']}")

    return df