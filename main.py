import flet as ft

class ToDoListApp:
    def __init__(self,page:ft.Page):
        self.page = page
        self._setup_page()
        self._create_components()
        self._create_ui()

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
            on_click=lambda _: print("Hola"),
        )
        
        self.search_bar = ft.TextField(
            label="Buscar tareas...",
            focused_border_color="#1a5553",
            bgcolor="#29363F",
            label_style=ft.TextStyle(color="#88ABD4",weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(color="#88ABD4",weight=ft.FontWeight.BOLD),
            on_change=lambda _: print("El texto cambio"),
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
            on_click=self._close_app
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
        
        self.task_for_view =  ft.Container(
            ft.Row([
                ft.Text("TaskID. Título De La Tarea",color="#88ABD4",weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.Text("12:30 01/01/26",color="#88ABD4",weight=ft.FontWeight.BOLD),
                ft.IconButton(ft.Icon(ft.Icons.DELETE_ROUNDED,color=ft.Colors.BLUE_300),width=110),
                ],
            margin=2,
            ),
            bgcolor="#1B262E",
            expand=True,
            padding=ft.Padding.only(left=10,right=20),
            shadow=ft.BoxShadow(spread_radius=2,blur_radius=2),
            ink=True,
            on_click=lambda _:print("Se presiono")
        )

        self.task_detail_taskid = ft.Text("• TaskID",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)
        self.task_detail_title = ft.Text("• Title Task",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)
        self.task_detail_date = ft.Text("• 12:30 01/01/26",weight=ft.FontWeight.BOLD,color="#88ABD4",size=16)
        
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


    def _second_plane_app(self):
        #TERMINAR FUNCIONALIDAD 
        print("Segundo Plano")
        
    async def _close_app(self):
        #TERMINAR FUNCIONALIDAD
        await self.page.window.close()

    def _change_value_menu_items(self,e:ft.Event[ft.PopupMenuItem]):
        e.control.checked = not e.control.checked
        selected_filters = [item.content.value for item in self.menu_filter_list_items if item.checked]
        if not selected_filters:
            e.control.checked = True
            selected_filters = [e.control.content.value]
        self.filter_text.value = f"Filtrar por: {", ".join(selected_filters)}"
        self.page.update()

    def _create_ui(self):
        
        task_view_card_title = ft.Container(
            ft.Row([
                ft.Icon(ft.Icons.ASSIGNMENT_ROUNDED,color=ft.Colors.BLUE_300),
                ft.Text("TAREAS",color="#88ABD4",weight=ft.FontWeight.BOLD,style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)),
                ]
            ),
        )
        
        task_view_all_card = ft.Container(
            ft.ListView(
                controls=[self.task_for_view for i in range(60)],
                padding=ft.Padding.only(top=10,left=5,right=5,bottom=30),
                width=650,
                height=280,
                scroll=ft.Scrollbar(thumb_visibility=True,thickness=10),
                spacing=8,
            ),
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
            

def main(page:ft.Page):
    app = ToDoListApp(page)

ft.run(main)