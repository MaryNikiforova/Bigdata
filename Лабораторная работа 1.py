import csv

# Функция Map для группировки данных по возрасту и полу и подсчета количества самоубийств
def map_func(record):
    age = record["age"]
    sex = record["sex"]
    suicides_no = int(record["suicides_no"])  
    return (age, sex), suicides_no

# Функция Reduce для суммирования количества самоубийств по каждой комбинации возраста и пола
def reduce_func(grouped_data):
    key, values = grouped_data
    total_suicides = sum(values)
    return key, total_suicides

# Основной код для выполнения MapReduce
def main():
    with open('master.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        age_sex_data = {}  
        for row in csv_reader:
            key, value = map_func(row)
            age_sex_data.setdefault(key, []).append(value)

        results = []
        for key, value in age_sex_data.items():
            result = reduce_func((key, value))
            results.append(result)

        # Сортировка результатов по количеству самоубийств в порядке убывания
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

        # Вывод результатов
        for (age, sex), total_suicides in sorted_results:
            print(f"Age: {age}, Sex: {sex}, Total Suicides: {total_suicides}")

if __name__ == "__main__":
    main()

