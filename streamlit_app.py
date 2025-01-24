import streamlit as st
import requests
import json


# Функция для выполнения POST-запроса
def send_post_request(data):
    url = "http://91.197.98.134:5000/get-next-move"
    headers = {"Content-Type": "application/json"}

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, json=data)

    # Обработка ответа
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Ошибка {response.status_code}: {response.text}"}


# Основная часть Streamlit приложения
def main():
    st.title("Тестовый запрос с использованием POST")

    # Ввод данных для запроса через интерфейс Streamlit
    api_key = st.text_input("Введите API ключ", "f91d8f74-61f3-4d3b-9b95-e4268d0e9f4e")
    grid = st.text_area("Введите грид (в формате JSON)", '''
    [
        ["b", "b", "r", "p", "y", "g"],
        ["y", "g", "b", "r", "p", "y"],
        ["b", "r", "p", "y", "g", "b"],
        ["r", "p", "y", "g", "b", "r"],
        ["p", "y", "g", "b", "r", "p"],
        ["y", "g", "b", "r", "p", "y"]
    ]
    ''')
    mode = st.selectbox("Выберите режим", ["gather", "fight", "other"])
    is_easy_fight = st.checkbox("Легкая битва", value=True)

    # Когда пользователь нажимает кнопку
    if st.button("Отправить запрос"):
        try:
            # Преобразуем введенный грид в список
            grid_data = json.loads(grid)

            # Подготовка данных для запроса
            data = {
                "api_key": api_key,
                "grid": grid_data,
                "mode": mode,
                "is_easy_fight": is_easy_fight
            }

            # Отправка POST-запроса
            result = send_post_request(data)

            # Показать результат
            st.subheader("Ответ от сервера:")
            st.json(result)

        except json.JSONDecodeError:
            st.error("Ошибка в формате JSON для грида.")
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()

