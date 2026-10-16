import os
import random
import pandas as pd


def _get_csv_path():
  """Helper to find the database relative to this script."""
  base_dir = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(base_dir, "LootDB.csv")


def get_all_categories():
  """Reads the CSV on startup to find all unique Category types."""
  try:
    df = pd.read_csv(_get_csv_path())
    if "Category" in df.columns:
      # Clear blanks/NaNs, get unique items, sort alphabetically
      cats = df["Category"].dropna().unique().tolist()
      return sorted([str(c) for c in cats])
    return []
  except:
    return []


def generate_loot(
    num_items: int,
    target_tier: int,
    target_category: str = "All",
    include_blox: bool = False,
):
  try:
    df = pd.read_csv(_get_csv_path())

    # 1. Filter down strictly to the selected Tier
    tier_df = df[df["Tier"] == target_tier]

    # 2. NEW: Filter down by Category if a specific one is picked
    if target_category != "All" and "Category" in tier_df.columns:
      tier_df = tier_df[tier_df["Category"].astype(str) == target_category]

    # 3. Filter out BLOX items if the box is left unticked
    if "BLOX" in tier_df.columns and not include_blox:
      tier_df = tier_df[tier_df["BLOX"].fillna(0).astype(int) != 1]

    if tier_df.empty:
      return [
          {
              "Item": f"No items found matching Tier {target_tier} ({target_category}) constraints.",
              "Category": "System",
          }
      ]

    # 4. Extract weights and perform choice mapping
    weights = (
        pd.to_numeric(tier_df["Weight"], errors="coerce").fillna(0).tolist()
    )
    items = tier_df.to_dict(orient="records")

    # 5. Roll random items matching probabilities
    selected_loot = random.choices(items, weights=weights, k=num_items)
    return selected_loot

  except Exception as e:
    return [{"Item": f"Error rolling loot: {str(e)}", "Category": "System"}]
