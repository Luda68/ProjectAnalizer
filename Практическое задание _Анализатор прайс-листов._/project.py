# import os
# import json
# import csv
#
#
# class PriceMachine():
#
#     def __init__(self):
#         self.data = []
#         self.result = ''
#         self.name_length = 0
#
#     def load_prices(self, file_path=''):
#         '''
#             Сканирует указанный каталог. Ищет файлы со словом price в названии.
#             В файле ищет столбцы с названием товара, ценой и весом.
#             Допустимые названия для столбца с товаром:
#                 товар
#                 название
#                 наименование
#                 продукт
#
#             Допустимые названия для столбца с ценой:
#                 розница
#                 цена
#
#             Допустимые названия для столбца с весом (в кг.)
#                 вес
#                 масса
#                 фасовка
#         '''
#
#     def _search_product_price_weight(self, headers):
#         '''
#             Возвращает номера столбцов
#         '''
#
#     def export_to_html(self, fname='output.html'):
#         result = '''
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>Позиции продуктов</title>
#         </head>
#         <body>
#             <table>
#                 <tr>
#                     <th>Номер</th>
#                     <th>Название</th>
#                     <th>Цена</th>
#                     <th>Фасовка</th>
#                     <th>Файл</th>
#                     <th>Цена за кг.</th>
#                 </tr>
#         '''
#
#     def find_text(self, text):
#
#
# pm = PriceMachine()
# print(pm.load_prices())
#
# '''
#     Логика работы программы
# '''
# print('the end')
# print(pm.export_to_html())


import os
import csv

class PriceMachine:
    def __init__(self):
        self.result = '' # результат последнего поиска
        self.data = []   # список для хранения данных
        self.selected_data = []  # список для хранения выбранных данных
        self.headers = ['name', 'price', 'weight', 'price_per_kg']

    def load_prices(self, file_path='./'):   # Сканирует указанный каталог и загружает данные из "price"-файлов
        for filename in os.listdir(file_path):
            if 'price' in filename and filename.endswith('.csv'):
                with open(os.path.join(file_path, filename), newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    headers = next(reader)
                    name_col = self._search_product_price_weight(headers, ['название', 'продукт', 'товар', 'наименование'])
                    price_col = self._search_product_price_weight(headers, ['цена', 'розница'])
                    weight_col = self._search_product_price_weight(headers, ['фасовка', 'масса', 'вес'])

                    for row in reader:
                        try:
                            name = row[name_col]
                            price = float(row[price_col])
                            weight = float(row[weight_col])
                            price_per_kg = price / weight
                            self.data.append({
                                'name': name,
                                'price': price,
                                'weight': weight,
                                'file': filename,
                                'price_per_kg': price_per_kg
                            })
                        except (IndexError, ValueError):
                            continue

    def _search_product_price_weight(self, headers, acceptable_names): # Возвращает индексы столбцов для названия товара, цены и веcа
        for index, header in enumerate(headers):
            if header in acceptable_names:
                return index
        return None

    def find_text(self, search_text): # Выполняет поиск по тексту в названии товара и сохраняет результаты
        if not search_text:
            self.selected_data = self.data
            return

        self.selected_data = [p for p in self.data if search_text.lower() in p['name'].lower()]
        self.selected_data.sort(key=lambda x: x['price_per_kg'])
        return

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
            <style>
                table {
                    border-collapse: collapse;
                }
                th, td {
                    padding: 8px;
                    border: 1px solid black;
                }
            </style>
        </head>
        <body>
            <table>
                <tr>
                    <th>№</th>
                    <th>Наименование</th>
                    <th>цена</th>
                    <th>вес</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        if not self.selected_data:    # фильтрация и сортировка данных
            self.selected_data = self.data

        for idx, item in enumerate(self.selected_data, start=1):
            result += f"<tr><td>{idx}</td><td>{item['name']}</td><td>{item['price']}</td><td>{item['weight']}</td><td>{item['file']}</td><td>{item['price_per_kg']:.2f}</td></tr>"

        result += '</table></body></html>'

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

    def print_results(self):
        if not self.selected_data:
            print("Товары не найдены.")
            return

        headers = {
            'idx': '№',
            'name': 'Наименование',
            'price': 'цена',
            'weight': 'вес',
            'price_per_kg': 'Цена за кг.'
        }

# форматирование таблицы
        col_widths = {header: max(len(headers[header]), max(len(str(item[header])) for item in self.selected_data)) for
                      header in self.headers}
        col_widths['idx'] = max(len(headers['idx']),
                                max(len(str(idx)) for idx in range(1, len(self.selected_data) + 1)))

        print(" | ".join(f"{headers[header].ljust(col_widths[header])}" for header in ['idx'] + self.headers))
        print("-+-".join('-' * col_widths[header] for header in ['idx'] + self.headers))

        for idx, item in enumerate(self.selected_data, start=1):
            print(
                f"{str(idx).ljust(col_widths['idx'])} | " +
                " | ".join(f"{str(item[header]).ljust(col_widths[header])}" for header in self.headers)
            )


analyzer = PriceMachine()
analyzer.load_prices()

while True:
    search = input("Введите текст для поиска (или 'exit' для выхода): ")
    if search.lower() == 'exit':
        print("Работа завершена.")
        analyzer.export_to_html()
        break

    analyzer.find_text(search)
    analyzer.print_results()
