# Canteen Sales Program — File I/O Assignment

Student Name: [Your Name]
Registration Number: [Your Reg No]
Course / Class: [Your Course]
Date Submitted: [Date]

---

## 1. Overview

This project is the individual Python File I/O assignment (20 marks).
It reads a hand-typed canteen sales file, rejects bad records without
crashing, writes a clean sales report, and demonstrates appending,
`seek()`/`tell()`, and missing-file handling.

Built with **only the Python standard library** — no `csv` or
`pandas` — to practise working with raw text lines.

---

## 2. Files in this submission

| File          | Purpose |
|---------------|---------|
| `canteen.py`  | All Part B and Part C code. Runnable with `python canteen.py`. |
| `sales.txt`   | Input data file (14 lines: header, one blank line, two faulty lines, and the new sale added in B5). |
| `report.txt`  | Output — clean sales report, produced by `canteen.py`. |
| `errors.txt`  | Output — every rejected line with its line number and reason. |
| `answers.txt` | Written answers for Part A (Q1–Q3) and Part C3, plus evidence for B5, C1 and C2. |
| `README.md`   | This file. |

---

## 3. How to run

```bash
python canteen.py
The program will:

Read sales.txt.

Skip the header and blank lines, strip whitespace, and convert
qty and price to integers.

Reject malformed lines (wrong field count or non-integer numbers)
and write them to errors.txt — the program does not crash.

Total quantity and revenue per item.

Write report.txt with items in alphabetical order and a grand
total row (overwrites any previous report).

Print a console summary: accepted records, rejected records,
total quantity, total revenue.

Demo the file position with readline(), tell() and seek(0),
and count every physical line (header and blanks included).

Expected console output
text
--- Canteen Sales Summary ---
Accepted records : 10
Rejected records : 2
Total quantity   : 185
Total revenue    : KES 3,605

--- File Position Demo (Part C2) ---
Header: 'date,item,qty,unit_price'
tell() after header: 25
Total lines (including header and blanks): 14
Expected report.txt
text
CAMPUS CANTEEN - SALES REPORT
Item        Qty  Revenue (KES)
Beans        18          1,080
Chapati      47            940
Mandazi      43            430
Tea          77          1,155
TOTAL       185          3,605
Expected errors.txt
text
Line 8: 2026-11-03,Tea,twenty,15 -> quantity 'twenty' is not an integer
Line 12: 2026-11-04,Chapati,9 -> expected 4 fields, found 3
4. How the marking criteria are met
Task	Requirement	Where
B1	with + encoding="utf-8", skip header, ignore blanks, ints stored	load_sales
B2	Both faulty lines rejected with correct line numbers and reasons; program keeps running	load_sales → errors.txt
B3	Correct qty and revenue per item	totals_by_item
B4	Report opened in write mode, sorted alphabetically, aligned columns, grand total	write_report
B5	Append mode used; invalid values refused; report updates	add_sale
C1	Friendly FileNotFoundError message	main()
C2	readline(), tell(), seek(0), line count	file_position_demo
C3	Reflection on text-file limitation and DB migration	answers.txt
5. Demonstrating B5 (adding a new sale)
The shipped sales.txt already contains the B5 sale
2026-11-05,Tea,25,15. To prove the append works without erasing
history:

Delete that last line (leaving 13 lines).

Run python canteen.py — note Tea qty = 52, revenue = 780.

In a Python shell, run:

python
from canteen import add_sale
add_sale("sales.txt", "2026-11-05", "Tea", 25, 15)
Run python canteen.py again — Tea qty = 77, revenue = 1,155.

add_sale raises ValueError for zero or negative qty/price.

6. Demonstrating C1 (missing file)
bash
mv sales.txt sales_backup.txt
python canteen.py
Console prints (no traceback):

text
Error: The file 'sales.txt' was not found. Please make sure it is in the current directory.
Restore with:

bash
mv sales_backup.txt sales.txt
