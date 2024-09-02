Задача 1:
grep '^[^:]' /etc/passwd | cut -d: -f1 | sort

Задача 2:
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n5

Задача 3:
#!/bin/bash

text=$*
length=${#text}

# Формирование символов рамки от 1 до длины слова + 2 пробела
for _ in $(seq 1 $((length + 2))); do
    line+="-"
done

echo "+${line}+"
echo "| ${text} |"
echo "+${line}+"
