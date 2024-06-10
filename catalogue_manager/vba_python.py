from openpyxl import Workbook
from openpyxl import load_workbook

# Create a new workbook
wb = load_workbook(filename='formular2.xlsm', read_only=False, keep_vba=True)
ws = wb["Sheet1"]

# Merge cells
ws.merge_cells('A1:A2')  # Merge cells A1 to B2
# ws['A1'] = 'Merged Cells'  # Add content to the merged cells

# Save the workbook
wb.save(filename='formular2.xlsm')
wb.close()