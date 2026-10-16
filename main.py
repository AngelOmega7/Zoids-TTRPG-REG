import flet as ft
import generator  # Imports your core logic script safely


def main(page: ft.Page):
    page.title = "Zoids TTRPG Tools"
    page.theme_mode = ft.ThemeMode.DARK

    # Common Subtitle used on both pages
    def create_subtitle():
        return ft.Text("Zoids TTRPG", size=16, italic=True, color=ft.Colors.BLUE_300)

    # --- SHARED UI DATA HOOKS ---
    encounter_results = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
    level_input = ft.TextField(
        label="Enter Encounter Level (1-50)",
        value="1",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=250,
        text_align="center"
    )

    def on_generate_click(e):
        encounter_results.controls.clear()
        try:
            lvl = int(level_input.value)
            if lvl < 1 or lvl > 50:
                raise ValueError
        except ValueError:
            encounter_results.controls.append(
                ft.Text("Please enter a valid integer between 1 and 50.", color=ft.Colors.RED_400)
            )
            render_view()
            return

        spawned_mob = generator.generate_encounter(lvl)
        if not spawned_mob:
            encounter_results.controls.append(ft.Text("No Zoids found matching this level criteria."))
        else:
            encounter_results.controls.append(
                ft.Text(f"Generated {len(spawned_mob)} Enemies:", size=16, weight=ft.FontWeight.NORMAL)
            )
            for zoid in spawned_mob:
                hp_tracker = ft.TextField(
                    value=str(zoid['HP']),
                    width=70,
                    height=30,
                    text_size=14,
                    content_padding=5,
                    text_align="center",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    border_color=ft.Colors.GREEN_700,
                    color=ft.Colors.GREEN_400
                )
                card = ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Column([
                            ft.Text(zoid['Name'], size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200),
                            ft.Row([
                                ft.Text(f"LV: {zoid['LV']}", weight=ft.FontWeight.NORMAL),
                                ft.Row([
                                    ft.Text("HP:", color=ft.Colors.GREEN_400, size=14),
                                    hp_tracker
                                ], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                ft.Text(f"Armor: {zoid['AR']}", color=ft.Colors.ORANGE_400),
                                ft.Text(f"Def: {zoid['DF']}", color=ft.Colors.PURPLE_300),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER)
                        ], spacing=5)
                    )
                )
                encounter_results.controls.append(card)
        render_view()  # Smoothly updates layout tree values

    generate_btn = ft.Button(
        "Generate Encounter",
        on_click=on_generate_click,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700
    )

    # --- DYNAMIC VIEWS WITH WORKING COLUMN SCROLLING ---
    def get_encounter_layout():
        return ft.Container(
            content=ft.Column([
                ft.Text("Random Encounter Generator", size=28, weight=ft.FontWeight.BOLD),
                create_subtitle(),
                ft.Divider(height=20, color="transparent"),
                level_input,
                generate_btn,
                ft.Divider(height=20, color="transparent"),
                encounter_results
            ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ADAPTIVE  # Keep scroll configuration strictly inside the Column
            ),
            expand=True
        )

    def get_loot_layout():
        return ft.Container(
            content=ft.Column([
                ft.Text("Random Loot Generator", size=28, weight=ft.FontWeight.BOLD),
                create_subtitle(),
                ft.Divider(height=20, color="transparent"),
                ft.Text("Loot generation parameters coming soon...", size=16, color=ft.Colors.GREY_400)
            ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ADAPTIVE  # Keep scroll configuration strictly inside the Column
            ),
            expand=True
        )

    # --- ROUTING APPLICATION DISPATCHER ---
    def render_view():
        page.controls.clear()

        if nav_bar.selected_index == 0:
            page.add(get_encounter_layout())
        elif nav_bar.selected_index == 1:
            page.add(get_loot_layout())

        page.update()

    def on_nav_change(e):
        render_view()

    nav_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.SHIELD, label="Encounters"),
            ft.NavigationBarDestination(icon=ft.Icons.CASINO, label="Loot"),
        ]
    )

    page.navigation_bar = nav_bar
    render_view()


if __name__ == "__main__":
    ft.run(main)



