#include <iostream>
#include <vector>
#include <list>
#include <string>
#include <Windows.h>
using namespace std;

// Структура для представления студента
struct Student {
    int bookNumber;   // Номер зачетной книжки (ключ)
    int groupNumber;  // Номер группы
    string name;      // ФИО

    Student(int book, int group, const string& fio)
        : bookNumber(book), groupNumber(group), name(fio) {}
};

// Хеш-таблица с цепным хешированием
class HashTable {
private:
    vector<list<Student*>> table;  // Массив списков указателей для разрешения коллизий
    int numElements;               // Количество элементов
    int capacity;                  // Размер таблицы (емкость)

    // Хеш-функция
    int hashFunction(int key) const {
        return key % capacity;
    }

    // Рехеширование при увеличении таблицы
    void rehash() {
        cout << "Рехеширование таблицы..." << endl;
        vector<list<Student*>> oldTable = table;
        capacity *= 2;  // Увеличиваем размер таблицы в 2 раза
        table.clear();
        table.resize(capacity);
        numElements = 0;

        for (const auto& bucket : oldTable) {
            for (const auto& studentPtr : bucket) {
                insert(studentPtr->bookNumber, studentPtr->groupNumber, studentPtr->name);
                delete studentPtr;  // Удаляем старый объект
            }
        }
    }

public:
    // Конструктор
    HashTable(int initialCapacity = 7) : capacity(initialCapacity), numElements(0) {
        table.resize(capacity);
    }

    // Деструктор для очистки динамически выделенной памяти
    ~HashTable() {
        for (auto& bucket : table) {
            for (auto& studentPtr : bucket) {
                delete studentPtr;  // Освобождаем память каждого студента
            }
        }
    }

    // Вставка элемента в хеш-таблицу
    void insert(int bookNumber, int groupNumber, const string& name) {
        if (numElements >= capacity) {
            rehash();
        }
        int index = hashFunction(bookNumber);
        table[index].push_back(new Student(bookNumber, groupNumber, name));
        numElements++;
        cout << "Студент " << name << " добавлен в таблицу." << endl;
    }

    // Поиск студента по номеру зачетной книжки
    bool search(int bookNumber) const {
        int index = hashFunction(bookNumber);
        for (const auto& studentPtr : table[index]) {
            if (studentPtr->bookNumber == bookNumber) {
                cout << "Найден студент: " << studentPtr->name << ", Группа: " << studentPtr->groupNumber << endl;
                return true;
            }
        }
        cout << "Студент с номером зачетной книжки " << bookNumber << " не найден." << endl;
        return false;
    }

    // Удаление студента по номеру зачетной книжки
    void remove(int bookNumber) {
        int index = hashFunction(bookNumber);
        for (auto it = table[index].begin(); it != table[index].end(); ++it) {
            if ((*it)->bookNumber == bookNumber) {
                cout << "Студент " << (*it)->name << " удален из таблицы." << endl;
                delete* it;  // Освобождаем память удаляемого объекта
                table[index].erase(it);
                numElements--;
                return;
            }
        }
        cout << "Студент с номером зачетной книжки " << bookNumber << " не найден." << endl;
    }

    // Вывод всех элементов таблицы
    void display() const {
        for (int i = 0; i < capacity; ++i) {
            cout << "Ячейка " << i << ": ";
            if (table[i].empty()) {
                cout << "пусто" << endl;
            }
            else {
                for (const auto& studentPtr : table[i]) {
                    cout << "[" << studentPtr->bookNumber << ", " << studentPtr->groupNumber << ", " << studentPtr->name << "] ";
                }
                cout << endl;
            }
        }
    }
};

// Текстовый интерфейс пользователя
void userInterface(HashTable& hashTable) {
    int choice;
    while (true) {
        cout << "\nВыберите действие:\n";
        cout << "1. Добавить студента\n";
        cout << "2. Удалить студента\n";
        cout << "3. Найти студента\n";
        cout << "4. Вывести таблицу\n";
        cout << "5. Выйти\n";
        cout << "Ваш выбор: ";
        cin >> choice;

        switch (choice) {
        case 1: {
            int bookNumber, groupNumber;
            string name;
            cout << "Введите номер зачетной книжки: ";
            cin >> bookNumber;
            cout << "Введите номер группы: ";
            cin >> groupNumber;
            cin.ignore();
            cout << "Введите ФИО: ";
            getline(cin, name);
            hashTable.insert(bookNumber, groupNumber, name);
            break;
        }
        case 2: {
            int bookNumber;
            cout << "Введите номер зачетной книжки для удаления: ";
            cin >> bookNumber;
            hashTable.remove(bookNumber);
            break;
        }
        case 3: {
            int bookNumber;
            cout << "Введите номер зачетной книжки для поиска: ";
            cin >> bookNumber;
            hashTable.search(bookNumber);
            break;
        }
        case 4: {
            hashTable.display();
            break;
        }
        case 5:
            return;
        default:
            cout << "Неверный выбор. Попробуйте снова." << endl;
        }
    }
}

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    HashTable hashTable;
    setlocale(LC_ALL, "rus");
    // Автоматическое заполнение таблицы
    hashTable.insert(1001, 1, "Иванов Иван Иванович");
    hashTable.insert(1002, 2, "Петров Петр Петрович");
    hashTable.insert(1003, 1, "Сидоров Сидор Сидорович");
    hashTable.insert(1004, 3, "Кузнецова Мария Ивановна");
    hashTable.insert(1005, 2, "Волков Алексей Сергеевич");

    userInterface(hashTable);

    return 0;
}
