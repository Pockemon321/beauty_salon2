import plantuml

# Создаем экземпляр PlantUML
plantuml_server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')

# Генерируем диаграмму
plantuml_server.processes_file('database_schema.puml', outfile='database_schema.png') 