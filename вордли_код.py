import flet as ft
import random
import time

matrix = []
num = 0
rows = []
загаданное_слово = ""
text = ft.Text(value = "", theme_style=ft.TextThemeStyle.TITLE_LARGE)
green = "green"
yellow = "yellow"

def main(page:ft.Page):
    # фокусирование на следующие текстовые поля
    def change_text(e):
        global num
        if len(e.control.value) == 1:
            for i in range(5):
                if e.control == matrix[num][i]:
                    if i == 4:
                        matrix[num][i].focus()
                    else:
                        matrix[num][i+1].focus()
        else:
            for i in range(5):
                if e.control == matrix[num][i]:
                    if i == 0:
                        matrix[num][i].focus()
                    else:
                        matrix[num][i-1].focus()

    # функция которая просто закрывает диалоговое окно при нажатии кнопки нет на диалоговом окне              
    def close_dlg(e):
        dlg_modal.open = False
        page.update()
        
    # функция которая выполняет код при нажатии кнопки "Тема" 
    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
        
    # создание диалогового окна   
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Сессия будет завершена"),
        content=ft.Text("Вы действительно хотите этого?"),
        actions=[
            ft.TextButton("Yes", on_click=lambda e: changetheme()),
            ft.TextButton("No", on_click=close_dlg)],
        actions_alignment=ft.MainAxisAlignment.END)
    
    # функция которая выполняет код при нажатии кнопки да на диалоговом окне
    def changetheme():
        global green, yellow
        dlg_modal.open = False
        page.splash.visible = True
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        green = "#ee82ee" if page.theme_mode == "dark" else "green"
        yellow = "#6a5acd" if page.theme_mode == "dark" else "yellow"
        page.update()
        time.sleep(0.5)
        toggledarklight.selected = True if page.theme_mode == "dark" else False
        page.splash.visible = False
        page.update()
        build()
        update()
        
    # создание текстовых полей
    def build():
        global загаданное_слово, num, matrix, rows, text, green, yellow
        matrix = []
        num = 0
        rows = []
        text.value = ""
        загаданное_слово = загадка()
        
        for i in range(7):
            mas = []
            for j in range(5):
                result = ft.TextField(value="", read_only=True, text_align=ft.TextAlign.CENTER, width=55, capitalization=ft.TextCapitalization.CHARACTERS, max_length=1, counter_text=" ", bgcolor="grey_500", on_change=change_text)
                mas.append(result)
            matrix.append(mas)
        matrix[6][0].bgcolor = green
        matrix[6][1].bgcolor = yellow
        matrix[6][2].bgcolor = "grey"

        for i in range(5):
            matrix[0][i].read_only = False

        for i in range(6):
            row = ft.Row([matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3], matrix[i][4]], alignment=ft.MainAxisAlignment.CENTER)
            rows.append(row)

    # функция для кнопки "Заново"   
    def restart(e):
        build()
        update()  

    # проверка существует ли введенное слово    
    def проверка(word):
        with open('слова.txt', 'r', encoding='utf-8') as file:
            if word == "":
                return False
            for line in file:
                if word+"\n" == line:
                    return True
            return False

    # функция которая загадывает слово
    def загадка():
        with open('слова.txt', 'r', encoding='utf-8') as file:
            слова = file.readlines()
        загаданное_слово = random.choice(слова).strip()
        print(загаданное_слово)
        return загаданное_слово

    # main
    def start(e):
        global загаданное_слово, num, matrix, text, green, yellow
        word = ""
        for i in range(5):
            word += matrix[num][i].value
        word = word.lower()
        if проверка(word) == False:
            text.value = "Нет такого слова"
            page.update()
        else:
            text.value = ""
            if num < 5:
                for i in range(5):
                    matrix[num][i].read_only=True
                    matrix[num + 1][i].read_only=False
            yellow_str = ""
            времено_загаданное_слово = загаданное_слово
            for i in range(5):
                if word[i] in времено_загаданное_слово:
                    if word[i] == времено_загаданное_слово[i]:
                        matrix[num][i].bgcolor=green
                        времено_загаданное_слово = времено_загаданное_слово[:i] + "_" + времено_загаданное_слово[i+1:]
                        yellow_str = yellow_str + "_"
                    else:
                        matrix[num][i].bgcolor=yellow
                        yellow_str = yellow_str + word[i]
                else:
                    matrix[num][i].bgcolor="grey"
                    yellow_str = yellow_str + "_"        
            if yellow_str != "":    
                for i in range(5):
                    if yellow_str[i]=="_":
                        continue
                    elif yellow_str[i] in времено_загаданное_слово:
                        for j in range(5):
                            if yellow_str[i] == времено_загаданное_слово[j]:
                                времено_загаданное_слово = времено_загаданное_слово[:j] + "_" + времено_загаданное_слово[j+1:]            
                                break
                    else:
                        matrix[num][i].bgcolor="grey"        
                    
            if word == загаданное_слово:
                text.value = "Вы отгадали слово"
                while num != 5:
                    for i in range(5):
                        matrix[num + 1][i].read_only=True
                        matrix[num + 1][i].bgcolor="grey"
                    num += 1
            elif num == 5:
                text.value = f"Не удалось угадать слово, было загадано слово {загаданное_слово}"
            num += 1
            page.update()

    # создание кнопки которая меняет тему
    toggledarklight = ft.IconButton(
		on_click=open_dlg_modal,
		icon="dark_mode",
		selected_icon="light_mode",
                selected=False, 
		style=ft.ButtonStyle(
		color={"":ft.colors.BLACK,"selected":ft.colors.WHITE}))

    # (переход между страницами) (заполнение страниц)
    def update():
        global rows, text
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Меню"), bgcolor=ft.colors.SURFACE_VARIANT,center_title = True, actions=[toggledarklight]),
                    ft.Row([ft.OutlinedButton(text="Играть",on_click = lambda _: page.go("/play"))],alignment = ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.OutlinedButton(text="Правила",on_click = lambda _: page.go("/rules"))],alignment = ft.MainAxisAlignment.CENTER),
                ]
            )
        )
        if page.route == "/play":
            page.views.append(
                ft.View(
                    "/play",
                    [
                        ft.AppBar(title=ft.Text("Вордли"), bgcolor=ft.colors.SURFACE_VARIANT,center_title = True),
                        rows[0], rows[1], rows[2] ,rows[3] ,rows[4], rows[5], ft.Row([ft.OutlinedButton(text="Проверить",on_click = start)],alignment = ft.MainAxisAlignment.CENTER), ft.Row([ft.OutlinedButton(text="Заново",on_click = restart)],alignment = ft.MainAxisAlignment.CENTER), ft.Row([text],alignment = ft.MainAxisAlignment.CENTER),
                    ]
                )
            )
        elif page.route == "/rules":
            page.views.append(
                ft.View(
                    "/rules",
                    [
                        ft.AppBar(title=ft.Text("Правила"), bgcolor=ft.colors.SURFACE_VARIANT,center_title = True),
                        ft.Row([ft.Text(value = "1)Введите любое существующее слово и нажмите 'Проверить'\n2)Буквы на игровом поле будут выделены разным цветом\n3)Вводите слова пока не отгадаете загаданное слово, или пока не закончатся попытки", theme_style=ft.TextThemeStyle.TITLE_LARGE)],alignment = ft.MainAxisAlignment.CENTER),
                        ft.Row([matrix[6][0],ft.Text(value = "Буква угадана верно                                                                                                  ", theme_style=ft.TextThemeStyle.TITLE_LARGE)],alignment = ft.MainAxisAlignment.CENTER),
                        ft.Row([matrix[6][1],ft.Text(value = "Буква есть в загаданном слове, но на другой позиции                                          ", theme_style=ft.TextThemeStyle.TITLE_LARGE)],alignment = ft.MainAxisAlignment.CENTER),
                        ft.Row([matrix[6][2],ft.Text(value = "Такой буквы нет в загаданном слове                                                                       ", theme_style=ft.TextThemeStyle.TITLE_LARGE)],alignment = ft.MainAxisAlignment.CENTER),
                    ]
                )
            )
        page.update()

    # (переход между страницами  
    def route_change(e):
        update()

    # (переход между страницами   
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    build()
    page.title = "Вордли"
    page.theme_mode = "light"
    page.splash = ft.ProgressBar(visible=False)
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target = main)
