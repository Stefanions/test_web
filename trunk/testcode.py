import json
import pandas as pd
from openpyxl import load_workbook

# Загружаем данные из JSON
with open('sp_EFRSB_parse/output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Фильтруем данные
filtered_json = [item for item in data if item['winner'] != ""]

# Преобразуем в DataFrame
df = pd.DataFrame(filtered_json)

# Сохраняем в Excel
excel_path = 'output.xlsx'
df.to_excel(excel_path, index=False)

# Загружаем файл Excel с помощью openpyxl
wb = load_workbook(excel_path)
ws = wb.active

# Растягиваем столбцы по ширине контента
for col in ws.columns:
    max_length = 0
    column = col[0].column_letter  # Получаем букву столбца
    for cell in col:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2)  # Добавляем немного пространства
    ws.column_dimensions[column].width = adjusted_width

# Сохраняем изменения
wb.save(excel_path)
