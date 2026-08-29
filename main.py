import flet as ft
import datetime
from backend import ToDoList

class ToDoListApp:
    def __init__(self,page:ft.Page):
        self.page = page
        self._setup_page()
        self._create_components()
        self._create_ui()
        self._show_all_task()
        self._change_add_task_date_label()

    def _setup_page(self):
        self.page.title = "Lista De Tareas"
        self.page.window.width = 1000
        self.page.window.height = 550
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme
        self.page.window.resizable = False
        self.page.window.maximizable = False
        self.page.padding = 25
    
    async def _open_menu(self):
        await self.menu_filter.open()
    
    def _create_components(self):
        
        self.menu_filter_items = {
            "pending" : ft.PopupMenuItem(ft.Text("Pendientes",color="#88ABD4"),checked=True,on_click=self._change_value_menu_items),
            "completed" : ft.PopupMenuItem(ft.Text("Completadas",color="#88ABD4"),checked=True ,on_click=self._change_value_menu_items),
        }
        
        self.menu_filter_list_items = [
            self.menu_filter_items["pending"],
            self.menu_filter_items["completed"],
        ]
         
        self.btn_add_task = ft.Button(
            ft.Row([
                ft.Text("Añadir Tarea",color="#88ABD4",size=15,weight=ft.FontWeight.BOLD),
                ft.Icon(ft.Icons.ADD,ft.Colors.BLUE_300)
            ],alignment=ft.MainAxisAlignment.CENTER),
            width = 200,
            bgcolor="#29363F",
            style=ft.ButtonStyle(
                overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(color="#1a5553"),
            ),
            on_click=lambda _: self.page.show_dialog(self.menu_add_task),
        )
        
        self.search_bar = ft.TextField(
            label="Buscar tareas...",
            focused_border_color="#1a5553",
            bgcolor="#29363F",
            label_style=ft.TextStyle(color="#88ABD4",weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(color="#88ABD4",weight=ft.FontWeight.BOLD),
            on_change=self._show_all_task,
            border_radius=15,
            height= 46,
            icon=ft.Icon(ft.Icons.SEARCH_ROUNDED,color=ft.Colors.BLUE_300),
            border_color="#268a87"
        )
        
        self.menu_filter = ft.ContextMenu(
            ft.IconButton(ft.Icons.SETTINGS_ROUNDED,icon_color="#88ABD4",on_click=self._open_menu),
            items=self.menu_filter_list_items,
        )
        
        self.filter_text = ft.Text(
            value="Filtrar Por: Pendientes, Completadas",
            color="#88ABD4",
            weight=ft.FontWeight.BOLD
        )
        
        self.btn_exit = ft.Button(ft.Row([
            ft.Icon(ft.Icons.CLOSE_ROUNDED,color=ft.Colors.BLUE_300),
            ft.Text("Salir",color="#88ABD4",weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            style=ft.ButtonStyle(
                overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(color="#1a5553"),
            ),
            on_click=self._close_app_gui
        )
        
        self.btn_second_plane = ft.Button(ft.Row([
            ft.Icon(ft.Icons.SYNC_ROUNDED,color=ft.Colors.BLUE_300),
            ft.Text("Segundo Plano",color="#88ABD4",weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER), 
            style=ft.ButtonStyle(
                overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(color="#1a5553"),
            ),
            on_click=self._second_plane_app,
            
        )

        self.task_detail_taskid = ft.Text("• TaskID",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)
        self.task_detail_title = ft.Text("• Title Task",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)
        self.task_detail_date = ft.Text("• 12:30 01/01/26",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)

        self.add_task_label_date= ft.Text(weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)        
        self.add_task_name = ft.TextField(
            label="Nombre De La Tarea",
            focused_border_color="#1a5553",
            bgcolor="#29363F",
            label_style=ft.TextStyle(color="#88ABD4",weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(color="#88ABD4",weight=ft.FontWeight.BOLD),
            border_radius=15,
            height= 46,
            border_color="#268a87",
        )
        self.add_task_date = ft.DatePicker(
            first_date=datetime.datetime.today(),
            help_text="Ingresa Una Fecha",
            field_hint_text="12/31/2026",
            cancel_text="Cancelar",
            confirm_text="Aceptar",
            field_label_text="Fecha De La Tarea",
            error_invalid_text="Esta Fecha Ya Ha Pasado",
            error_format_text="Formato De Fecha Ivalido",
            on_change=self._change_add_task_date_label,
            value=datetime.datetime.today()
            )
        self.add_task_time = ft.TimePicker(
            value=datetime.datetime.now().time(),
            help_text="Ingresa Una Hora",
            cancel_text="Cancelar",
            confirm_text="Aceptar",
            error_invalid_text="Coloca Una Hora Valida",
            hour_label_text="Hora(s)",
            minute_label_text="Minuto(s)",
            on_change=self._change_add_task_date_label
            )
        
        self.btn_complete_task = ft.Button(
            ft.Row([
                ft.Icon(ft.Icons.CHECK_ROUNDED,ft.Colors.BLUE_300),
                ft.Text("Completar",color="#88ABD4",),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(color="#1a5553"),
            )
        )
        
        self.btn_modify_task = ft.Button(
            ft.Row([
                ft.Icon(ft.Icons.EDIT_ROUNDED,ft.Colors.BLUE_300),
                ft.Text("Modificar",color="#88ABD4",),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(color="#1a5553"),
            )
        )
        
        self.btn_delete_all = ft.Button(
            ft.Row([
                ft.Icon(ft.Icons.DELETE_FOREVER_ROUNDED,ft.Colors.BLUE_300),
                ft.Text("Eliminar Tareas Completadas",color="#88ABD4",),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(color="#1a5553"),
            )
        )

        self.list_view_tasks = ft.ListView(
            controls=[],
            padding=ft.Padding.only(top=10,left=5,right=5,bottom=30),
            width=650,
            height=280,
            scroll=ft.Scrollbar(thumb_visibility=True,thickness=10),
            spacing=8,
        )

    def _second_plane_app(self):
        #TERMINAR FUNCIONALIDAD 
        print("Segundo Plano")
        
    async def _close_app_gui(self):
        #TERMINAR FUNCIONALIDAD
        await self.page.window.close()

    def _change_add_task_date_label(self):
        self.add_task_label_date.value = "• "+self.add_task_date.value.strftime("%d/%m/%Y")+" "+self.add_task_time.value.strftime("%H:%M")

    def _change_value_menu_items(self,e:ft.Event[ft.PopupMenuItem]):
        e.control.checked = not e.control.checked
        selected_filters = [item.content.value for item in self.menu_filter_list_items if item.checked]
        if not selected_filters:
            e.control.checked = True
            selected_filters = [e.control.content.value]
        self.filter_text.value = f"Filtrar por: {", ".join(selected_filters)}"
        self._show_all_task()
        self.page.update()

    def _add_task(self):
        if not self.add_task_name.value:
            return
        to_do_list_backend.añadir_tarea(self.add_task_name.value.strip(),self.add_task_date.value.strftime("%Y-%m-%d ")+self.add_task_time.value.strftime("%H:%M"))
        self.show_all_task()

    def _change_task_detail(self,e:ft.ControlEvent):
        self.task_detail_taskid.value = "• "+str(e.control.content.controls[0].value)
        self.task_detail_title.value = "• "+e.control.content.controls[1].value
        self.task_detail_date.value = "• "+e.control.content.controls[3].value

    def delete_task(self,e:ft.ControlEvent):
        to_do_list_backend.eliminar_tarea(e.control.parent.controls[0].value)
        self._show_all_task()

    def _show_all_task(self):
        filter_parameter = 1 if self.menu_filter_items["completed"].checked and not self.menu_filter_items["pending"].checked else 0
        filter_parameter_checked = None if self.menu_filter_items["completed"].checked == self.menu_filter_items["pending"].checked else 0
        tasks_for_view = []
        for task in to_do_list_backend.buscar_tarea(self.search_bar.value,self.search_bar.value,filter_parameter_checked,filter_parameter):
            tasks_for_view.append(ft.Container(
                ft.Row([
                    ft.Text(task[0],color="#88ABD4",weight=ft.FontWeight.BOLD),
                    ft.Text(f"- {task[1]}",color="#88ABD4",weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Text(task[2],color="#88ABD4",weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icon(ft.Icons.DELETE_ROUNDED,color=ft.Colors.BLUE_300),width=110,on_click=self.delete_task),
                    ],
                margin=2,
                ),
                bgcolor="#1B262E",
                expand=True,
                padding=ft.Padding.only(left=10,right=20),
                shadow=ft.BoxShadow(spread_radius=2,blur_radius=2),
                ink=True,
                on_click=self._change_task_detail,
            ))
        self.list_view_tasks.controls = tasks_for_view
        self.page.update()

    def _create_ui(self):
        
        self.menu_add_task = ft.AlertDialog(
            ft.Column(
                [
                    ft.Divider(color="#0DA98C",radius=10,thickness=2),
                    self.add_task_name,
                    ft.Button(
                        ft.Row([
                            ft.Text("Fecha A Avisar",color="#88ABD4",size=15,weight=ft.FontWeight.BOLD),
                            ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED,ft.Colors.BLUE_300)
                        ],alignment=ft.MainAxisAlignment.CENTER),
                        width = 250,
                        bgcolor="#29363F",
                        style=ft.ButtonStyle(
                            overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=ft.BorderSide(color="#1a5553"),
                        ),
                        on_click=lambda:self.page.show_dialog(self.add_task_date),
                    ),
                    ft.Button(
                        ft.Row([
                            ft.Text("Hora A Avisar",color="#88ABD4",size=15,weight=ft.FontWeight.BOLD),
                            ft.Icon(ft.Icons.SCHEDULE_ROUNDED,ft.Colors.BLUE_300)
                        ],alignment=ft.MainAxisAlignment.CENTER),
                        width = 250,
                        bgcolor="#29363F",
                        style=ft.ButtonStyle(
                            overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=ft.BorderSide(color="#1a5553"),
                        ),
                        on_click=lambda:self.page.show_dialog(self.add_task_time),
                    ),
                    self.add_task_label_date,
                    ft.Divider(color="#0DA98C",radius=10,thickness=2),
                    ft.Row(
                        [
                            ft.Button(  
                                ft.Row([
                                    ft.Text("Aceptar",color="#88ABD4",size=15,weight=ft.FontWeight.BOLD),
                                    ft.Icon(ft.Icons.CHECK_BOX_ROUNDED,ft.Colors.BLUE_300)
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                style=ft.ButtonStyle(
                                    overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    side=ft.BorderSide(color="#1a5553"),
                                ),
                                on_click=self._add_task,
                            ),
                            ft.Button(  
                                ft.Row([
                                    ft.Text("Cancelar",color="#88ABD4",size=15,weight=ft.FontWeight.BOLD),
                                    ft.Icon(ft.Icons.DELETE_SWEEP_ROUNDED,ft.Colors.BLUE_300)
                                ],alignment=ft.MainAxisAlignment.CENTER),
                                style=ft.ButtonStyle(
                                    overlay_color={ft.ControlState.PRESSED:"#2B456C"},
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    side=ft.BorderSide(color="#1a5553"),
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN   
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                height=255,
            ),
        alignment=ft.Alignment.TOP_LEFT,
        actions_alignment=ft.MainAxisAlignment.CENTER,
        title=ft.Text("Crear Una Nueva Tarea",weight=ft.FontWeight.BOLD,color="#88ABD4",size=19,style=(ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,decoration_color="#268a87",))),
        title_padding=ft.Padding(left=74,top=27,bottom=3),
        )
        
        task_view_card_title = ft.Container(
            ft.Row([
                ft.Icon(ft.Icons.ASSIGNMENT_ROUNDED,color=ft.Colors.BLUE_300),
                ft.Text("TAREAS",color="#88ABD4",weight=ft.FontWeight.BOLD,style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,)),
                ]
            ),
        )
        
        task_view_all_card = ft.Container(
            self.list_view_tasks,
            bgcolor="#29363F",
            shadow=ft.BoxShadow(spread_radius=2,blur_radius=2,color="#1a5553")
        )
        
        task_detail_card = ft.Container(
            ft.Column([
                ft.Text("Detalles De La Tarea",
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(
                            decoration=ft.TextDecoration.UNDERLINE,
                            decoration_color="#268a87",
                            weight=ft.FontWeight.BOLD,
                            size=18,
                            ),
                        color="#88ABD4",
                        align=ft.Alignment.TOP_CENTER
                    ),
                ft.Divider(color="#0DA98C",radius=10,thickness=2),
                self.task_detail_taskid,
                self.task_detail_title,
                self.task_detail_date,
                self.btn_modify_task,
                self.btn_complete_task,
                ],
            spacing=20
            )
        )
        
        self.page.add(
            ft.Container(
                ft.Row(
                    controls=[
                        self.btn_add_task,
                        ft.Container(expand=True),
                        self.search_bar,
                        self.menu_filter,
                    ],
                ),
            ),
            ft.Row(self.filter_text,alignment=ft.MainAxisAlignment.END),
            ft.Row([
                ft.Column([
                    task_view_card_title,
                    task_view_all_card,
                    ]
                ),
                ft.Column([
                    task_detail_card,
                    ],
                    expand=True,
                ),
                ],
                vertical_alignment=ft.MainAxisAlignment.START
            ),
            ft.Column(
                ft.Row(
                    controls=[
                        self.btn_exit,
                        self.btn_second_plane,
                        ft.Container(expand=True),
                        self.btn_delete_all,
                        ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    expand=True,
                    ),
                expand=True
            ),
        )

to_do_list_backend = ToDoList()

def main(page:ft.Page):
    app = ToDoListApp(page)

ft.run(main)