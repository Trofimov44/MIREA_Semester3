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

