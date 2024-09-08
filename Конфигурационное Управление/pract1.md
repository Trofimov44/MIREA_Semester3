![изображение](https://github.com/user-attachments/assets/be6fcc64-ab64-402d-bf29-2d1464482e1a)Задача 1:
grep '^[^:]' /etc/passwd | cut -d: -f1 | sort

Задача 2:
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n5

Задача 3:
