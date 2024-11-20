from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def wait_for_shadow_root(driver):
    """Wait for and return the shadow root of the bc-data-grid element."""
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "bc-data-grid"))
        )
        shadow_root = driver.execute_script("return document.querySelector('bc-data-grid').shadowRoot")
        if not shadow_root:
            raise Exception("Shadow root not found")
        return shadow_root
    except Exception as e:
        raise Exception(f"Error locating shadow root: {e}")

def extract_headers(shadow_root):
    """Extract and return the headers from the shadow root."""
    header_cells = shadow_root.find_elements(By.CSS_SELECTOR, ".bc-datatable-header-tooltip")
    headers = [header.text for header in header_cells]
    return headers

def extract_rows(driver):
    """Extract rows from the shadow DOM."""
    rows = driver.execute_script("""
        const shadowRoot = document.querySelector('bc-data-grid')?.shadowRoot;
        if (!shadowRoot) return null;
        return Array.from(shadowRoot.querySelectorAll("set-class.row[role='row']"));
    """)
    if not rows:
        raise Exception("No rows found in shadow DOM")
    return rows

def extract_cells(driver, row):
    """Extract cells from a row."""
    cells = driver.execute_script("return Array.from(arguments[0].querySelectorAll('div._cell'));", row)
    if not cells:
        raise Exception("No cells found in the row")
    return cells

def extract_cell_text(driver, cell):
    """Extract text from a cell."""
    return driver.execute_script("""
        const textBinding = arguments[0].querySelector('text-binding');
        if (textBinding?.shadowRoot) {
            return textBinding.shadowRoot.textContent.trim();
        }
        return 'No text found';
    """, cell)
