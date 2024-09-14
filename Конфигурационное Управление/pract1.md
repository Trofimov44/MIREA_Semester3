# Задача1:
```
grep '^[^:]' /etc/passwd | cut -d: -f1 | sort
```
![изображение](https://github.com/user-attachments/assets/5b65586e-c155-40fd-8559-111ee92509fc)


# Задача 2:
```
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n5
```
![изображение](https://github.com/user-attachments/assets/ffe2388b-8ff5-4af2-9e06-bad6e960dff7)

# Задача 3:
```
#!/bin/bash
text="$1"
text_length=${#text}
echo "+"$(printf -- '-%.0s' $(seq 1 $((text_length + 2))))"+"
echo "| $text |"
echo "+"$(printf -- '-%.0s' $(seq 1 $((text_length + 2))))"+"
```

![изображение](https://github.com/user-attachments/assets/f47e79d5-866d-4e38-90e6-03529f084104)

# Задача 4:
```
grep -oE '\b[A-Za-z_][A-Za-z0-9_]*\b' main.cpp | sort -u
```
![изображение](https://github.com/user-attachments/assets/d22e13f6-617d-4398-8c44-f8c65625d2da)


# Задача 5:
```
#!/bin/bash
if [ -z "$1" ]; then
      echo "реализация задания с помощью команд "
        #ls -l /usr/local/bin/reg
  #reg banner
      exit 1
    fi

    prog_name="$1"
    dest="/usr/local/bin/$prog_name"

    # проверка- существует ли программа
    if [ ! -f "$prog_name" ]; then
      echo "файл $prog_name не найден."
      exit 1
    fi

    # копирование в /usr/local/bin и установка прав доступа
    sudo cp "$prog_name" "$dest"
    sudo chmod 755 "$dest"

    echo "программа $prog_name успешно зарегистрирована в /usr/local/bin."

  #ls -l /usr/local/bin/reg
  #reg banner
```
![изображение](https://github.com/user-attachments/assets/24e7a5cd-eda3-4ce2-93c6-8707f7b2f3ba)

# Задача 6:
```
#!/bin/bash
for file in *.{c,js,py}; do
  if [ -f "$file" ]; then
    first_line=$(head -n 1 "$file")
    if [[ "$first_line" == /* ]] || [[ "$first_line" == \#* ]] || [[ "$first_line" == "//"* ]]; then
      echo "$file: комментарий найден в первой строке."
    else
      echo "$file: комментарий не найден."
    fi
  fi
done
```
![изображение](https://github.com/user-attachments/assets/b336e7f2-61a9-4b6a-9072-2cac0b53de96)

# Задача 7:
```
#!/bin/bash

    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "использование: $0 <путь> <расширение>"
        exit 1
    fi

    search_path="$1"
    extension="$2"
    archive_name="archive_$extension.tar"

    if [ ! -d "$search_path" ]; then
        echo "путь $search_path не существует или не является директорией"
        exit 1
    fi

    echo "архивирование файлов с расширением $extension из $search_path в $archive_name..."
    find "$search_path" -type f -name "*.$extension" | tar -cvf "$archive_name" -T -

    echo "
архив $archive_name создан"
```
![изображение](https://github.com/user-attachments/assets/a0c242ea-6548-49f7-9e62-03aad7160073)

