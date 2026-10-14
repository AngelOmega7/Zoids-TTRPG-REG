import flet as ft
import generator  # Imports your core logic script safely

def main(page: ft.Page):
    # App Settings & Theming Layout
    page.title = "Random Encounter Generator"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.DARK

    # Header Controls 
    title = ft.Text("Random Encounter Generator", size=28, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Zoids TTRPG", size=16, italic=True, color=ft.Colors.BLUE_300)
    
    # Input field capturing target difficulty tiers
    level_input = ft.TextField(
        label="Enter Encounter Level (1-50)",
        value="1",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=250,
        text_align=ft.TextAlign.CENTER
    )
    
    # Display container where results inject smoothly
    results_column = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    # Click handler reacting locally without top-to-bottom script refreshes
    def on_generate_click(e):
        results_column.controls.clear()
        
        # User input sanitation check
        try:
            lvl = int(level_input.value)
            if lvl < 1 or lvl > 50:
                raise ValueError
        except ValueError:
            results_column.controls.append(
                ft.Text("Please enter a valid integer between 1 and 50.", color=ft.Colors.RED_400)
            )
            page.update()
            return
        
        # Fetch data arrays directly from the engine module
        spawned_mob = generator.generate_encounter(lvl)
        
        if not spawned_mob:
            results_column.controls.append(ft.Text("No Zoids found matching this level criteria."))
        else:
            results_column.controls.append(
                ft.Text(f"Generated {len(spawned_mob)} Enemies:", size=16, weight=ft.FontWeight.W_500)
            )
            
            # Map dictionary payloads cleanly into standard Flutter card objects
            for zoid in spawned_mob:
                card = ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Column([
                            ft.Text(zoid['Name'], size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200),
                            ft.Row([
                                ft.Text(f"LV: {zoid['LV']}", weight=ft.FontWeight.W_500),
                                ft.Text(f"HP: {zoid['HP']}", color=ft.Colors.GREEN_400),
                                ft.Text(f"Armor: {zoid['AR']}", color=ft.Colors.ORANGE_400),
                                ft.Text(f"Def: {zoid['DF']}", color=ft.Colors.PURPLE_300),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ], spacing=5)
                    )
                )
                results_column.controls.append(card)
                
        page.update()  # Direct state update dispatch trigger

    generate_btn = ft.ElevatedButton(
        "Generate Encounter", 
        on_click=on_generate_click,
        style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700)
    )

    # Compile layout nodes into viewport
    page.add(
        title,
        subtitle,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        level_input,
        generate_btn,
        ft.Divider(height=20),
        results_column
    )

if __name__ == "__main__":
    try:
        ft.main(main)
    except AttributeError:
        ft.app(target=main)
