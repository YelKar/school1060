import string

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles.borders import Border, Side
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell


def generate(titles: list, *sheets: list[list[str]]):
    wb = Workbook()
    del wb["Sheet"]
    ws: Worksheet = wb.create_sheet("Test")
    print(ws.column_dimensions["A"].width)
    for num, title in enumerate(titles, 1):
        cell: Cell = ws.cell(1, num, title)
        cell.value = title
        cell.font = Font(bold=True)
        cell.border = Border(
            left=Side(style="medium"),
            right=Side(style="medium"),
            top=Side(style="medium"),
            bottom=Side(style="medium"),
        )
        ws.column_dimensions[
            string.ascii_uppercase[num - 1]
        ].width = len(title) + 2
    wb.save("generated/xlsx/test.xlsx")


if __name__ == '__main__':
    generate(
        [
            f"Заголовок{t}" for t in [1, 2, 2343, 546264356, 56375477547]
        ], None
    )
