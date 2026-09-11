"""Interfaz gráfica Flet para gestionar tareas de escritorio en Windows.

Este módulo construye los controles y coordina eventos de usuario con la
capa de negocio de ``backend.py``. No contiene consultas SQL directas.
"""

import flet as ft
import datetime
from backend import ToDoList

class ToDoListApp:
    """Controlador de la ventana principal y sus diálogos de tareas."""

    def __init__(self,page:ft.Page):
        """Inicializa la página, controles, diálogos y listado de tareas.

        Args:
            page: Página Flet que alojará la aplicación.
        """
        self.page = page
        self._setup_page()
        self.task_detail_notified_value = None
        self._create_components()
        self._create_ui()
        self._show_all_task()
        self._change_add_task_date_label()
        self._change_modify_task_date_label()

    def _setup_page(self):
        """Configura tamaño, tema, icono y comportamiento de la ventana."""
        self.page.title = "Lista De Tareas"
        self.page.window.width = 1000
        self.page.window.height = 550
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.resizable = False
        self.page.window.maximizable = False
        self.page.padding = 25
        self.page.window.icon = str(to_do_list_backend.path_icon)
    
    async def _open_menu(self):
        """Abre el menú contextual de filtros."""
        await self.menu_filter.open()
    
    def _create_components(self):
        """Crea controles reutilizables y sus callbacks de interacción."""
        
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
        self.task_detail_name = ft.Text("• Title Task",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)
        self.task_detail_datetime = ft.Text("• 12:30 01/01/26",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)
        self.task_detail_notified = ft.Text("• Notifi: ",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)

        self.add_task_label_datetime = ft.Text(weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)        
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

        self.modify_task_label_datetime = ft.Text(weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)        
        self.modify_task_name = ft.TextField(
            label="Nombre De La Tarea",
            focused_border_color="#1a5553",
            bgcolor="#29363F",
            label_style=ft.TextStyle(color="#88ABD4",weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(color="#88ABD4",weight=ft.FontWeight.BOLD),
            border_radius=15,
            height= 46,
            border_color="#268a87",
        )
        self.modify_task_date = ft.DatePicker(
            first_date=datetime.datetime.today(),
            help_text="Ingresa Una Fecha",
            field_hint_text="12/31/2026",
            cancel_text="Cancelar",
            confirm_text="Aceptar",
            field_label_text="Fecha De La Tarea",
            error_invalid_text="Esta Fecha Ya Ha Pasado",
            error_format_text="Formato De Fecha Ivalido",
            on_change=self._change_modify_task_date_label,
            value=datetime.datetime.today()
            )
        self.modify_task_time = ft.TimePicker(
            value=datetime.datetime.now().time(),
            help_text="Ingresa Una Hora",
            cancel_text="Cancelar",
            confirm_text="Aceptar",
            error_invalid_text="Coloca Una Hora Valida",
            hour_label_text="Hora(s)",
            minute_label_text="Minuto(s)",
            on_change=self._change_modify_task_date_label
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
            ),
            on_click=self._complete_task,
            disabled=True,
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
            ),
            on_click=self._modify_btn_behavior,
            disabled=True,
        )
        
        self.btn_delete_all_completed = ft.Button(
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
            ),
            on_click=self.btn_delete_all_completed_behavior
        )

        self.list_view_tasks = ft.ListView(
            controls=[],
            padding=ft.Padding.only(top=10,left=5,right=5,bottom=30),
            width=650,
            height=280,
            scroll=ft.Scrollbar(thumb_visibility=True,thickness=10),
            spacing=8,
        )

    def btn_delete_all_completed_behavior(self):
        """Elimina tareas completadas y refresca el listado."""
        to_do_list_backend.delete_all_task_completed()
        self._show_all_task()

    def _show_gui_from_systemtray(self):
        """Restaura y enfoca la ventana desde la bandeja del sistema."""
        def restored():
            """Hace visible y enfoca la ventana restaurada."""
            self.page.window.minimized = False
            self.page.window.visible = True
            self.page.window.focused = True
            self.page.update()
        self.page.run_thread(restored)

    def _close_gui_from_system_tray(self):
        """Solicita el cierre de la aplicación desde la bandeja."""
        self.page.run_task(self._close_app_gui)
        self.page.update()

    def _second_plane_app(self):
        """Oculta la ventana y mantiene activo el icono de bandeja."""
        self.page.window.visible = False
        self.page.update()
        to_do_list_backend.start_system_tray(self._show_gui_from_systemtray,self._close_gui_from_system_tray)

    async def _close_app_gui(self):
        """Detiene el monitor de notificaciones y cierra la ventana."""
        to_do_list_backend.event_stop.set()
        await self.page.window.close()

    def _modify_btn_behavior(self):
        """Carga los datos seleccionados y abre el diálogo de edición."""
        self.modify_task_name.value = self.task_detail_name_value
        self.modify_task_label_datetime.value = self.task_detail_datetime.value
        self.page.show_dialog(self.menu_modify_task)

    def _change_modify_task_date_label(self):
        """Actualiza la etiqueta de fecha/hora del diálogo de edición."""
        self.modify_task_label_datetime.value = "• "+self.modify_task_date.value.strftime("%Y-%m-%d")+" "+self.modify_task_time.value.strftime("%H:%M")
    
    def _change_add_task_date_label(self):
        """Actualiza la etiqueta de fecha/hora del diálogo de creación."""
        self.add_task_label_datetime.value = "• "+self.add_task_date.value.strftime("%Y-%m-%d")+" "+self.add_task_time.value.strftime("%H:%M")

    def _change_value_menu_items(self,e:ft.Event[ft.PopupMenuItem]):
        """Alterna un filtro y evita que todos los filtros queden desactivados."""
        e.control.checked = not e.control.checked
        selected_filters = [item.content.value for item in self.menu_filter_list_items if item.checked]
        if not selected_filters:
            e.control.checked = True
            selected_filters = [e.control.content.value]
        self.filter_text.value = f"Filtrar por: {", ".join(selected_filters)}"
        self._show_all_task()

    def _add_task(self):
        """Valida el nombre, inserta la tarea y refresca el listado."""
        if not self.add_task_name.value:
            return
        to_do_list_backend.añadir_tarea(self.add_task_name.value.strip(),self.add_task_date.value.strftime("%Y-%m-%d ")+self.add_task_time.value.strftime("%H:%M"))
        self.page.pop_dialog()
        self._show_all_task()

    def _selected_task_detail(self,e:ft.ControlEvent):
        """Carga en el panel lateral la tarea seleccionada por el usuario."""
        self.task_detail_taskid_value = e.control.content.controls[0].value
        self.task_detail_name_value = e.control.content.controls[1].value
        self.task_detail_datetime_value = e.control.content.controls[3].value
        self.task_detail_notified_value = 0 if e.control.content.controls[4].value == "Notifi: No" else 1
        self.btn_modify_task.disabled = False
        self.btn_complete_task.disabled = False
        self._change_task_detail()

    def _complete_task(self,e=None):
        """Invierte el estado de la tarea seleccionada y actualiza la UI."""
        to_do_list_backend.modify_task_value_notified(self.task_detail_taskid_value)
        self.task_detail_notified_value = 1 - self.task_detail_notified_value
        self._change_task_detail()
        self._show_all_task()

    def _change_task_detail(self):
        """Pinta los datos del panel sin modificar el estado almacenado."""
        self.task_detail_taskid.value = "• "+str(self.task_detail_taskid_value)
        self.task_detail_name.value = "• "+str(self.task_detail_name_value)
        self.task_detail_datetime.value = "• "+self.task_detail_datetime_value
        if self.task_detail_notified_value == 0:
            self.task_detail_notified.value = "• Notificado: No"
            self.btn_complete_task.content = ft.Row([
                    ft.Icon(ft.Icons.CHECK_ROUNDED,ft.Colors.BLUE_300),
                    ft.Text("Completar",color="#88ABD4",),
                ],
                alignment=ft.MainAxisAlignment.CENTER,)
        else:
            self.task_detail_notified.value = "• Notificado: Si"
            self.btn_complete_task.content = ft.Row([
                ft.Icon(ft.Icons.CLOSE_ROUNDED,ft.Colors.BLUE_300),
                ft.Text("Sin Terminar",color="#88ABD4",),
                ],
                alignment=ft.MainAxisAlignment.CENTER,)
        self.page.update()

    def _modify_task(self):
        """Guarda los cambios de nombre y fecha de la tarea seleccionada."""
        date_for_modify = f"{self.modify_task_date.value.strftime("%Y-%m-%d")} {self.modify_task_time.value.strftime("%H:%M")}"
        self.task_detail_name_value = self.modify_task_name.value
        self.task_detail_datetime_value = date_for_modify
        to_do_list_backend.modify_task_value(self.modify_task_name.value,date_for_modify,self.task_detail_taskid_value)
        self.page.pop_dialog()
        self._change_task_detail()
        self._show_all_task()

    def delete_task(self,e:ft.ControlEvent):
        """Elimina la tarea de la tarjeta pulsada y refresca la interfaz."""
        if e.control.parent.controls[0].value == self.task_detail_taskid_value:
            self.task_detail_taskid.value = "• TaskID"
            self.task_detail_name.value = "• Title Task"
            self.task_detail_datetime.value = "• 12:30 01/01/26"
            self.btn_complete_task.disabled = True
            self.btn_modify_task.disabled = True
        to_do_list_backend.eliminar_tarea(e.control.parent.controls[0].value)
        self._show_all_task()

    def _show_all_task(self):
        """Consulta tareas según filtros/búsqueda y reconstruye la lista."""
        filter_parameter = 1 if self.menu_filter_items["completed"].checked and not self.menu_filter_items["pending"].checked else 0
        filter_parameter_checked = None if self.menu_filter_items["completed"].checked == self.menu_filter_items["pending"].checked else 0
        tasks_for_view = []
        for task in to_do_list_backend.search_task(self.search_bar.value,self.search_bar.value,filter_parameter_checked,filter_parameter):
            tasks_for_view.append(ft.Container(
                ft.Row([
                    ft.Text(task[0],color="#88ABD4",weight=ft.FontWeight.BOLD),
                    ft.Text(task[1],color="#88ABD4",weight=ft.FontWeight.BOLD,overflow=ft.TextOverflow.FADE,width=250),
                    ft.Container(expand=True),
                    ft.Text(task[2],color="#88ABD4",weight=ft.FontWeight.BOLD),
                    ft.Text("Notifi: Si" if task[3] == 1 else "Notifi: No",color="#88ABD4",weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icon(ft.Icons.DELETE_ROUNDED,color=ft.Colors.BLUE_300),width=110,on_click=self.delete_task),
                    ],
                margin=2,
                ),
                bgcolor="#1B262E",
                expand=True,
                padding=ft.Padding.only(left=10,right=20),
                shadow=ft.BoxShadow(spread_radius=2,blur_radius=2),
                ink=True,
                on_click=self._selected_task_detail,
            ))
        self.list_view_tasks.controls = tasks_for_view
        self.page.update()

    def _create_ui(self):
        """Construye diálogos, paneles y distribución principal de la página."""
        
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
                    self.add_task_label_datetime,
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
                                on_click=lambda:self.page.pop_dialog()
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
        
        self.menu_modify_task = ft.AlertDialog(
            ft.Column(
                [
                    ft.Divider(color="#0DA98C",radius=10,thickness=2),
                    self.modify_task_name,
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
                        on_click=lambda:self.page.show_dialog(self.modify_task_date),
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
                        on_click=lambda:self.page.show_dialog(self.modify_task_time),
                    ),
                    self.modify_task_label_datetime,
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
                                on_click=self._modify_task,
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
                            on_click=lambda:self.page.pop_dialog()
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN   
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                height=255,
            ),
        alignment=ft.Alignment.BOTTOM_RIGHT,
        actions_alignment=ft.MainAxisAlignment.CENTER,
        title=ft.Text("Editar La Tarea Seleccionada",weight=ft.FontWeight.BOLD,color="#88ABD4",size=19,style=(ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,decoration_color="#268a87",))),
        title_padding=ft.Padding(left=50,top=27,bottom=3),
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
                self.task_detail_name,
                self.task_detail_datetime,
                self.task_detail_notified,
                self.btn_modify_task,
                self.btn_complete_task,
                ],
            spacing=17
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
                        self.btn_delete_all_completed,
                        ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    expand=True,
                    ),
                expand=True
            ),
        )

to_do_list_backend = ToDoList()

def main(page:ft.Page):
    """Punto de entrada de Flet para crear la aplicación principal."""
    app = ToDoListApp(page)

ft.run(main)