# pylint: disable=invalid-name

"""
computeSales.py

Computes the total cost of all sales using:
1) A JSON price catalogue (list of products)
2) A JSON sales record (list of sales)

Outputs results to console and SalesResults.txt
"""

import json
import sys
import time
from typing import Any, Dict, Optional, List


RESULTS_FILE = "SalesResults.txt"


def load_json_file(filepath: str) -> Optional[Any]:
    """Loads a JSON file safely. Returns None if an error occurs."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
    except json.JSONDecodeError:
        print(f"[ERROR] Invalidx JSON format in file: {filepath}")
    except OSError as error:
        print(f"[ERROR] Cannot open file {filepath}: {error}")
    return None


def build_price_map(catalogue_data: Any) -> Dict[str, float]:
    """
    Builds a dictionary:
        product_title -> price

    Handles invalidx catalogue entries and continues.
    """
    price_map: Dict[str, float] = {}

    if not isinstance(catalogue_data, list):
        print("[ERROR] Price catalogue JSON must be a list of products.")
        return price_map

    for idx, item in enumerate(catalogue_data):
        if not isinstance(item, dict):
            print(f"[ERROR] Catalogue item #{idx} is not an object.")
            continue

        title = item.get("title")
        price = item.get("price")

        if not isinstance(title, str):
            print(f"[ERROR] Catalogue item #{idx} has invalidx 'title'.")
            continue

        if not isinstance(price, (int, float)):
            print(f"[ERROR] Catalogue item #{idx} has invalidx 'price'.")
            continue

        price_map[title] = float(price)

    return price_map


def compute_sales_total(price_map: Dict[str, float], sales_data: Any) -> float:
    """
    Computes total cost of all sales.

    Each sale record must contain:
        Product (str)
        Quantity (number)
    """
    total_cost = 0.0

    if not isinstance(sales_data, list):
        print("[ERROR] Sales record JSON must be a list of sales.")
        return total_cost

    for idx, sale in enumerate(sales_data):
        if not isinstance(sale, dict):
            print(f"[ERROR] Sale #{idx} is not an object.")
            continue

        product = sale.get("Product")
        quantity = sale.get("Quantity")

        if not isinstance(product, str):
            print(f"[ERROR] Sale #{idx}: invalidx 'Product'.")
            continue

        if not isinstance(quantity, (int, float)):
            print(f"[ERROR] Sale #{idx}: invalidx 'Quantity'.")
            continue

        if product not in price_map:
            print(
                f"[ERROR] Sale #{idx}: product '{product}' not in catalogue."
            )
            continue

        total_cost += price_map[product] * float(quantity)

    return total_cost


def format_results(total_cost: float, elapsed_seconds: float) -> str:
    """Creates a human-readable report."""
    lines: List[str] = []
    lines.append("==== SALES RESULTS ====")
    lines.append(f"Total Sales Cost: ${total_cost:,.2f}")
    lines.append("")
    lines.append(f"Time Elapsed: {elapsed_seconds:.6f} seconds")
    lines.append("=======================")
    return "\n".join(lines)


def write_results_file(content: str) -> None:
    """Writes results to SalesResults.txt safely."""
    try:
        with open(RESULTS_FILE, "w", encoding="utf-8") as file:
            file.write(content + "\n")
    except OSError as error:
        print(f"[ERROR] Could not write {RESULTS_FILE}: {error}")


def main() -> None:
    """Main execution entrypoint."""
    start_time = time.perf_counter()

    if len(sys.argv) != 3:
        print(
            "Usage:\n"
            "  python computeSales.py priceCatalogue.json salesRecord.json"
        )
        sys.exit(1)

    catalogue_path = sys.argv[1]
    sales_path = sys.argv[2]

    catalogue_data = load_json_file(catalogue_path)
    sales_data = load_json_file(sales_path)

    if catalogue_data is None or sales_data is None:
        print("[ERROR] Cannot proceed due to invalidx input files.")
        sys.exit(1)

    price_map = build_price_map(catalogue_data)
    total_cost = compute_sales_total(price_map, sales_data)

    elapsed_seconds = time.perf_counter() - start_time
    results_text = format_results(total_cost, elapsed_seconds)

    print(results_text)
    write_results_file(results_text)


if __name__ == "__main__":
    main()
