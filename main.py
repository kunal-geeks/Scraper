import pandas as pd
from futures_analysis.analyzer import clean_and_add_mean
from futures_analysis.driver import initialize_driver
from futures_analysis.extractor import wait_for_shadow_root, extract_headers, extract_rows, extract_cells, extract_cell_text
from futures_analysis.saver import save_to_excel
from futures_analysis.visualizer import plot_graph

# Adjust Pandas settings to display more rows and columns
pd.set_option('display.max_rows', None)  # No limit to the number of rows displayed
pd.set_option('display.max_columns', None)  # No limit to the number of columns displayed
pd.set_option('display.width', None)  # Adjust the width of the terminal output
pd.set_option('display.max_colwidth', None)  # Show full content in each cell

def main():
    try:
        # Initialize WebDriver
        driver = initialize_driver()

        # Step 2: Open the target webpage
        driver.get("https://www.barchart.com/futures")

        # Wait for the shadow root and extract headers
        shadow_root = wait_for_shadow_root(driver)
        headers = extract_headers(shadow_root)

        # Prepare to collect data
        rows = extract_rows(driver)

        table_data = []
        for index, row in enumerate(rows, start=1):
            cells = extract_cells(driver, row)
            row_data = [extract_cell_text(driver, cell) for cell in cells]
            table_data.append(row_data)

        # Print or process `table_data` as needed
        print("Data extraction complete.")

        # Step 5: Convert extracted data into a Pandas DataFrame
        df = pd.DataFrame(table_data, columns=headers)
        # Step 6: Call the analysis function to perform tasks like creating "Mean", plotting, and finding the largest "Change"
        df_with_mean = clean_and_add_mean(df)
        print(df_with_mean)

        # Step 7: Plot the data
        plot_graph(df_with_mean)

        # Step 8: Save the DataFrame to an Excel file
        # After all analysis
        save_to_excel(df_with_mean, "futures_market_analysis.xlsx")


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
