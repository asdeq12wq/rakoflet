import flet as ft
import math

def main(page: ft.Page):
    page.title = "حاسبة علمية متقدمة"
    page.window_width = 500
    page.window_height = 700
    page.theme_mode = "dark"

    # إضافة عنوان البرنامج
    title = ft.Text(
        value="محمد عبدالحسين كاظم",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_500,
        text_align="center"
    )

    result = ft.TextField(
        value="0",
        text_align="right",
        read_only=True,
        width=480,
    )

    history = ft.Text(value="", size=14, color=ft.colors.GREY_500)
    memory = 0
    current_number = []
    operation = None
    previous_number = 0
    new_number = True
    angle_mode = "DEG"  # or "RAD"

    def format_result(value):
        if value.is_integer():
            return str(int(value))
        return str(value)

    def update_history(entry):
        history.value += entry + "\n"
        page.update()

    def number_click(e):
        nonlocal new_number
        if new_number:
            result.value = ""
            new_number = False
        result.value = result.value + e.control.text
        page.update()

    def operation_click(e):
        nonlocal operation, previous_number, new_number
        operation = e.control.text
        previous_number = float(result.value)
        new_number = True
        page.update()

    def scientific_operation(e):
        nonlocal new_number
        try:
            current = float(result.value)
            op = e.control.text
            if op == "sin":
                val = math.sin(current if angle_mode == "RAD" else math.radians(current))
            elif op == "cos":
                val = math.cos(current if angle_mode == "RAD" else math.radians(current))
            elif op == "tan":
                val = math.tan(current if angle_mode == "RAD" else math.radians(current))
            elif op == "arcsin":
                val = math.degrees(math.asin(current)) if angle_mode == "DEG" else math.asin(current)
            elif op == "arccos":
                val = math.degrees(math.acos(current)) if angle_mode == "DEG" else math.acos(current)
            elif op == "arctan":
                val = math.degrees(math.atan(current)) if angle_mode == "DEG" else math.atan(current)
            elif op == "√":
                val = math.sqrt(current)
            elif op == "x²":
                val = current ** 2
            elif op == "x³":
                val = current ** 3
            elif op == "1/x":
                val = 1 / current
            elif op == "log":
                val = math.log10(current)
            elif op == "ln":
                val = math.log(current)
            elif op == "±":
                val = -current
            elif op == "π":
                val = math.pi
            elif op == "e":
                val = math.e
            elif op == "%":
                val = current / 100
            result.value = format_result(val)
            update_history(f"{op}({current}) = {result.value}")
            new_number = True
            page.update()
        except Exception as err:
            result.value = "Error"
            update_history(f"Error in operation: {e.control.text}")
            new_number = True
            page.update()

    def equals_click(e):
        nonlocal previous_number, new_number
        if operation:
            try:
                current = float(result.value)
                if operation == "+":
                    val = previous_number + current
                elif operation == "-":
                    val = previous_number - current
                elif operation == "×":
                    val = previous_number * current
                elif operation == "÷":
                    val = previous_number / current
                elif operation == "xʸ":
                    val = previous_number ** current
                elif operation == "ʸ√x":
                    val = previous_number ** (1 / current)
                result.value = format_result(val)
                update_history(f"{previous_number} {operation} {current} = {result.value}")
                new_number = True
                page.update()
            except:
                result.value = "Error"
                update_history("Error in calculation")
                new_number = True
                page.update()

    def memory_operation(e):
        nonlocal memory
        op = e.control.text
        current = float(result.value)
        if op == "M+":
            memory += current
            update_history(f"Memory + {current}")
        elif op == "M-":
            memory -= current
            update_history(f"Memory - {current}")
        elif op == "MR":
            result.value = format_result(memory)
            update_history(f"Memory Recall: {result.value}")
            new_number = True
        elif op == "MC":
            memory = 0
            update_history("Memory Cleared")
        page.update()

    def toggle_angle(e):
        nonlocal angle_mode
        angle_mode = "RAD" if angle_mode == "DEG" else "DEG"
        e.control.text = angle_mode
        page.update()

    def clear_click(e):
        nonlocal previous_number, operation, new_number
        result.value = "0"
        previous_number = 0
        operation = None
        new_number = True
        update_history("Cleared")
        page.update()

    def clear_history(e):
        history.value = ""
        page.update()

    # تنظيم الأزرار في مصفوفات
    scientific_buttons = [
        ["sin", "cos", "tan", "π"],
        ["arcsin", "arccos", "arctan", "e"],
        ["√", "x²", "x³", "xʸ"],
        ["log", "ln", "1/x", "ʸ√x"],
        ["M+", "M-", "MR", "MC"],
    ]

    number_buttons = [
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
    ]

    def create_button(text, color, on_click):
        return ft.ElevatedButton(
            text=text,
            bgcolor=color,
            on_click=on_click,
            width=90,
        )

    # إنشاء صفوف الأزرار العلمية
    scientific_rows = []
    for row in scientific_buttons:
        current_row = []
        for button in row:
            if button.startswith("M"):
                color = ft.colors.DEEP_PURPLE_700
                on_click = memory_operation
            else:
                color = ft.colors.INDIGO_700
                on_click = scientific_operation
            current_row.append(create_button(button, color, on_click))
        scientific_rows.append(ft.Row(controls=current_row, alignment=ft.MainAxisAlignment.CENTER))

    # إنشاء صفوف الأزرار الرقمية
    number_rows = []
    for row in number_buttons:
        current_row = []
        for button in row:
            if button in ["÷", "×", "-", "+", "xʸ", "ʸ√x"]:
                color = ft.colors.BLUE_700
                on_click = operation_click
            elif button == "=":
                color = ft.colors.ORANGE_700
                on_click = equals_click
            else:
                color = ft.colors.GREY_800
                on_click = number_click
            current_row.append(create_button(button, color, on_click))
        number_rows.append(ft.Row(controls=current_row, alignment=ft.MainAxisAlignment.CENTER))

    top_row = ft.Row(
        controls=[
            create_button("C", ft.colors.RED_700, clear_click),
            create_button("±", ft.colors.INDIGO_700, scientific_operation),
            create_button("%", ft.colors.INDIGO_700, scientific_operation),
            create_button(angle_mode, ft.colors.TEAL_700, toggle_angle),
            create_button("Clear History", ft.colors.RED_400, clear_history),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # إضافة كل العناصر للصفحة
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    title,
                    result,
                    top_row,
                    *scientific_rows,
                    *number_rows,
                    ft.Container(content=history, height=100, bgcolor=ft.colors.GREY_900, padding=10),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10
        )
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
                
