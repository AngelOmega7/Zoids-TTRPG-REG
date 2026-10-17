import flet as ft
import sys
import generator  # Imports your core logic script safely
import loot

def main(page: ft.Page):
    page.title = "Zoids TTRPG Tools"
    page.theme_mode = ft.ThemeMode.DARK
    # Responsive sizing is applied from page.on_resize below. Desktop keeps the
    # original dimensions; narrow screens use compact controls and stacked actions.
    is_mobile_layout = False
    control_width = 250
    if sys.platform == "win32":
        page.window.icon = "assets/icon.ico"
    # Common Subtitle used on both pages
    def create_subtitle():
        return ft.Text("Zoids TTRPG", size=16, italic=True, color=ft.Colors.BLUE_300)

    # --- SHARED ENCOUNTER UI DATA HOOKS ---
    encounter_results = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
    level_input = ft.TextField(
        label="Enter Encounter Level (1-50)",
        value="1",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=250,
        text_align="center"
    )

    # --- SHARED LOOT UI DATA HOOKS ---
    loot_results = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    loot_tier_dropdown = ft.Dropdown(
        label="Select Loot Tier",
        value="1",
        options=[
            ft.dropdown.Option("1"),
            ft.dropdown.Option("2"),
            ft.dropdown.Option("3"),
            ft.dropdown.Option("4"),
            ft.dropdown.Option("5"),
        ],
        width=250,
    )
    try:
      available_categories = ["All"] + loot.get_all_categories()
    except Exception:
      available_categories = ["All"]
    
    loot_category_dropdown = ft.Dropdown(
        label="Filter by Category",
        value="All",
        options=[ft.dropdown.Option(cat) for cat in available_categories],
        width=250,
    )

    loot_count_input = ft.TextField(
        label="Number of Items to Drop",
        value="1",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=250,
        text_align="center"
    )

    blox_checkbox = ft.Checkbox(
        label="Include BLOX Items",
        value=False
    )

    # --- CLICK HANDLERS ---
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
            page.update()  # Deep loop safe refresh
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
                                vertical_alignment=ft.CrossAxisAlignment.CENTER, wrap=True)
                        ], spacing=5)
                    )
                )
                encounter_results.controls.append(card)
        page.update()  # Direct inline layout tree refresh

    def on_generate_loot_click(e):
        loot_results.controls.clear()
        try:
            count = int(loot_count_input.value)
            tier = int(loot_tier_dropdown.value)
            category = str(loot_category_dropdown.value)  # Capture Category layout state
            if count < 1:
                raise ValueError
        except ValueError:
            loot_results.controls.append(
                ft.Text("Please enter a valid number of items greater than 0.", color=ft.Colors.RED_400)
            )
            page.update()
            return

        # 🚀 Updated to pass category selection straight down into loot.py
        dropped_items = loot.generate_loot(
            num_items=count,
            target_tier=tier,
            target_category=category,
            include_blox=blox_checkbox.value
        )

        if dropped_items and isinstance(dropped_items, list) and len(dropped_items) == 1 and "Error" in str(
                dropped_items[0].get('Item', '')):
            loot_results.controls.append(ft.Text(dropped_items[0]['Item'], color=ft.Colors.RED_400))
        else:
            loot_results.controls.append(
                ft.Text(f"Generated {len(dropped_items)} {category if category != 'All' else ''} Tier {tier} Items:",
                        size=16, weight=ft.FontWeight.NORMAL)
            )

            for item in dropped_items:
                blox_val = item.get('BLOX')
                is_blox_item = str(blox_val) == "1" or blox_val == 1.0 or blox_val == 1

                type_label = f"{item.get('Category', 'General')}"
                if is_blox_item:
                    type_label += " [BLOX]"

                card = ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Column([
                            ft.Text(
                                item.get('Item', 'Unknown Item'),
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.RED_200 if is_blox_item else ft.Colors.BLUE_200
                            ),
                            ft.Row([
                                ft.Text(f"Type: {type_label}", italic=True),
                                ft.Text(f"Tier {item.get('Tier', tier)}", color=ft.Colors.BLUE_300,
                                        weight=ft.FontWeight.BOLD),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ], spacing=5)
                    )
                )
                loot_results.controls.append(card)
        page.update()

    def on_random_category_click(e):
        import random
        # 1. Isolate just the actual game categories (skip the "All" filter)
        game_categories = [cat for cat in loot.get_all_categories() if cat != "All"]

        if not game_categories:
            page.overlay.append(ft.SnackBar(ft.Text("No categories found in LootDB.csv.")))
            page.update()
            return

        # 2. Pick a random category choice
        random_choice = random.choice(game_categories)

        # 3. Update the dropdown interface value automatically
        loot_category_dropdown.value = random_choice

        # 4. Display a clean popup notification toast to the user
        page.overlay.append(
            ft.SnackBar(
                content=ft.Text(f"Selected Random Category: {random_choice}", weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.BLUE_900,
                open=True
            )
        )
        page.update()

    # --- BUTTON DECLARATIONS ---
    generate_btn = ft.Button(
        "Generate Encounter",
        on_click=on_generate_click,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700
    )

    generate_loot_btn = ft.Button(
        "Roll Tier Loot",
        on_click=on_generate_loot_click,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700
    )

    random_category_btn = ft.Button(
        "Random Category",
        on_click=on_random_category_click,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREY_800
    )

    # --- PERSISTENT VIEW LAYOUTS ---
    encounter_heading = ft.Text("Random Encounter Generator", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    loot_heading = ft.Text("Random Loot Generator", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    category_controls = ft.Container(
        content=ft.Row([loot_category_dropdown, random_category_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        alignment=ft.alignment.center,
    )

    encounter_layout = ft.Column([
        encounter_heading,
        create_subtitle(),
        ft.Divider(height=20, color="transparent"),
        level_input,
        generate_btn,
        ft.Divider(height=20, color="transparent"),
        encounter_results
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.ADAPTIVE)

    loot_layout = ft.Column([
        loot_heading,
        create_subtitle(),
        ft.Divider(height=20, color="transparent"),
        loot_tier_dropdown,
        ft.Divider(height=10, color="transparent"),

        # The resize handler switches this between a row (desktop) and column (phone).
        category_controls,

        ft.Divider(height=10, color="transparent"),
        loot_count_input,
        ft.Divider(height=10, color="transparent"),
        blox_checkbox,
        ft.Divider(height=10, color="transparent"),
        generate_loot_btn,
        ft.Divider(height=20, color="transparent"),
        loot_results
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.ADAPTIVE)

    # --- FIXED MAIN CONTAINER ARCHITECTURE ---
    # We load a persistent parent container area instead of clear/adding nodes continuously
    main_view_container = ft.Container(content=encounter_layout, expand=True)

    def switch_tab(e):
        if nav_bar.selected_index == 0:
            main_view_container.content = encounter_layout
        elif nav_bar.selected_index == 1:
            main_view_container.content = loot_layout
        page.update()  # Safe view-swap content toggle trigger

    nav_bar = ft.NavigationBar(
        selected_index=0,
        on_change=switch_tab,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.SHIELD, label="Encounters"),
            ft.NavigationBarDestination(icon=ft.Icons.CASINO, label="Loot"),
        ]
    )

    page.navigation_bar = nav_bar
    page.add(main_view_container)  # Single core structural load instance

    def apply_responsive_layout(e=None):
        """Compact the UI on narrow screens without changing desktop sizing."""
        nonlocal is_mobile_layout, control_width
        screen_width = page.width or 800
        mobile = screen_width < 600
        is_mobile_layout = mobile
        control_width = max(180, min(250, int(screen_width - 40))) if mobile else 250

        # Inputs remain at their original 250px width on desktop.
        level_input.width = control_width
        loot_tier_dropdown.width = control_width
        loot_category_dropdown.width = control_width
        loot_count_input.width = control_width

        # Headings and spacing become more compact only on phones.
        heading_size = 21 if mobile else 28
        encounter_heading.size = heading_size
        loot_heading.size = heading_size
        encounter_layout.spacing = 6 if mobile else 10
        loot_layout.spacing = 6 if mobile else 10

        if mobile:
            category_controls.width = control_width
            category_controls.content = ft.Column(
                [loot_category_dropdown, ft.Container(content=random_category_btn, width=control_width)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            )
        else:
            category_controls.width = None
            category_controls.content = ft.Row(
                [loot_category_dropdown, random_category_btn],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )

        page.update()

    page.on_resize = apply_responsive_layout
    # Apply once after the initial layout; on_resize handles later rotation/resizing.
    apply_responsive_layout()


# --- UNIVERSAL PLATFORM DISPATCHER ---
if __name__ == "__main__":
    # Check if the active Flet version supports the new 'run' attribute
    if hasattr(ft, "run"):
        ft.run(main)  # Executes on your Flet 1.0+ Windows/Linux builds
    else:
        ft.app(target=main)  # Fallback for mobile environments running older Flet runtimes
