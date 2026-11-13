"""
CANTEEN SALES PROGRAM - File I/O Assignment
Student Name: KIBUCHI MAINA
Admission Number: 202617998
Course : A.P.T 

Reads sales.txt, validates records, writes report.txt and errors.txt,
and demonstrates append, tell()/seek() and missing-file handling.
"""


def load_sales(filename):
    """
    Read sales.txt and return a list of valid record dictionaries.
    Skips the header and blank lines. Invalid lines are collected and
    written to errors.txt with their original line numbers and reasons.
    """
    records = []
    errors = []

    with open(filename, "r", encoding="utf-8") as f:
        f.readline()               # skip the header (line 1)
        line_number = 1

        for raw_line in f:
            line_number += 1
            line = raw_line.strip()   # remove newline and surrounding spaces

            if not line:               # ignore blank lines
                continue

            fields = line.split(",")

            # B2: reject lines without exactly 4 fields
            if len(fields) != 4:
                errors.append((line_number, line,
                               f"expected 4 fields, found {len(fields)}"))
                continue

            date = fields[0].strip()
            item = fields[1].strip()
            qty_str = fields[2].strip()
            price_str = fields[3].strip()

            # B2: reject non-integer quantity or price, but keep going
            try:
                qty = int(qty_str)
                price = int(price_str)
            except ValueError:
                problems = []
                try:
                    int(qty_str)
                except ValueError:
                    problems.append(f"quantity '{qty_str}' is not an integer")
                try:
                    int(price_str)
                except ValueError:
                    problems.append(f"price '{price_str}' is not an integer")
                errors.append((line_number, line, "; ".join(problems)))
                continue

            records.append({
                "date": date,
                "item": item,
                "qty": qty,
                "price": price,
            })

    # Write every rejected line to errors.txt (overwritten each run)
    with open("errors.txt", "w", encoding="utf-8") as ef:
        for ln, orig, reason in errors:
            ef.write(f"Line {ln}: {orig} -> {reason}\n")

    return records


def totals_by_item(records):
    """
    Return {item: {"qty": total_qty, "revenue": total_revenue}}.
    """
    totals = {}
    for r in records:
        item = r["item"]
        if item not in totals:
            totals[item] = {"qty": 0, "revenue": 0}
        totals[item]["qty"] += r["qty"]
        totals[item]["revenue"] += r["qty"] * r["price"]
    return totals


def write_report(totals, filename):
    """
    Write report.txt with alphabetical item rows and a grand total row.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("CAMPUS CANTEEN - SALES REPORT\n")
        f.write(f"{'Item':<10}{'Qty':>5}{'Revenue (KES)':>15}\n")

        grand_qty = 0
        grand_rev = 0
        for item in sorted(totals):
            qty = totals[item]["qty"]
            rev = totals[item]["revenue"]
            f.write(f"{item:<10}{qty:>5}{rev:>15,}\n")
            grand_qty += qty
            grand_rev += rev

        f.write(f"{'TOTAL':<10}{grand_qty:>5}{grand_rev:>15,}\n")


def add_sale(filename, date, item, qty, price):
    """
    B5: Append one correctly formatted sale line to sales.txt.
    Refuses non-positive quantity or price.
    """
    if qty <= 0 or price <= 0:
        raise ValueError("Quantity and price must be positive integers.")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{date},{item},{qty},{price}\n")


def file_position_demo(filename):
    """
    C2: read the header with readline(), show tell(), then seek(0)
    and count every line (header and blanks included).
    """
    with open(filename, "r", encoding="utf-8") as f:
        header = f.readline()
        print(f"Header: {header.rstrip()!r}")
        print(f"tell() after header: {f.tell()}")
        f.seek(0)
        line_count = sum(1 for _ in f)
        print(f"Total lines (including header and blanks): {line_count}")


def main():
    sales_file = "sales.txt"

    # C1: friendly missing-file message instead of a traceback
    try:
        records = load_sales(sales_file)
    except FileNotFoundError:
        print(f"Error: The file '{sales_file}' was not found. "
              f"Please make sure it is in the current directory.")
        return

    # Count how many lines were rejected (written by load_sales)
    try:
        with open("errors.txt", "r", encoding="utf-8") as ef:
            rejected = sum(1 for line in ef if line.strip())
    except FileNotFoundError:
        rejected = 0

    totals = totals_by_item(records)
    write_report(totals, "report.txt")

    grand_qty = sum(t["qty"] for t in totals.values())
    grand_rev = sum(t["revenue"] for t in totals.values())

    print("--- Canteen Sales Summary ---")
    print(f"Accepted records : {len(records)}")
    print(f"Rejected records : {rejected}")
    print(f"Total quantity   : {grand_qty}")
    print(f"Total revenue    : KES {grand_rev:,}")

    # C2 demonstration
    print("\n--- File Position Demo (Part C2) ---")
    file_position_demo(sales_file)


if __name__ == "__main__":
    main()
    # B5 demonstration (uncomment once to add the extra sale, then re-run):
    # add_sale("sales.txt", "2026-11-05", "Tea", 25, 15)