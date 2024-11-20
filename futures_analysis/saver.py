import pandas as pd

def save_to_excel(df, file_name="output.xlsx"):
    """
    Saves the DataFrame to an Excel sheet efficiently and ensures all data is fully visible.
    """
    try:
        # Use ExcelWriter with openpyxl engine for faster and reliable saving
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            # Save the DataFrame
            df.to_excel(writer, sheet_name="Raw Data", index=False)

            # Access the workbook and sheet to adjust column widths
            workbook = writer.book
            worksheet = writer.sheets["Raw Data"]

            # Set column widths to accommodate data
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).map(len).max(), len(col)
                ) + 2  # Add extra padding
                worksheet.column_dimensions[chr(65 + idx)].width = max_length

        print(f"DataFrame successfully saved to '{file_name}'.")

    except Exception as e:
        print(f"Error saving to Excel: {e}")
