Задача 1:
grep '^[^:]' /etc/passwd | cut -d: -f1 | sort

Задача 2:
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n5

Задача 3:
