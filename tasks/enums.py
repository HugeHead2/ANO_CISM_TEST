from enum import StrEnum


class StatusEnum(StrEnum):
    new = "Новая задача"
    process = "В процессе работы"
    done = "Завершено успешно"
    error = "Ошибка"
