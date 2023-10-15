# prac_1
Построение по НКА ДКА и ПДКА

## Usage:
```shell
usage: main.py [-h] [--input <path>] [--input-format <format>] [--action <action>] [--alphabet <alpha> [<alpha> ...]] [--output <path>] [--output-format <format>]

options:
  -h, --help            show this help message and exit
  --input <path>, -i <path>
                        path to input file
  --input-format <format>, -if <format>
                        input file format
  --action <action>, -A <action>
                        action to do with imported automaton
  --alphabet <alpha> [<alpha> ...], -a <alpha> [<alpha> ...]
                        alphabet, required if full_* action specified
  --output <path>, -o <path>
                        path to output file
  --output-format <format>, -of <format>
                        output file format
```

### input
Входной файл. Если не указан, то вход будет считан из стандартного потока ввода

### input format
Поддерживается doa и regexp. Если не указан, то по умолчанию doa

### action
Действие которое необходимо произвести с автоматом:
#### reformat
Не производить преобразований, просто переписать данные в указанных форматах
#### determine
Построить ДКА по заданному автомату, доп. сведения не требуются
#### min_determine
Построить минДКА по заданному автомату, доп. сведения не требуются
#### full_*
Аналогично предыдущим, но дополняет автомат до полного. Требуется указать алфавит

### alphabet
Алфавит в котором работает автомат. Поддерживаются только строго одно буквенные алфавиты

### output, output format
Аналогично input, input format

### output format
Поддерживается doa и graphviz
