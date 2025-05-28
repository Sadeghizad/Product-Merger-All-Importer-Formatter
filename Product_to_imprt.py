import pandas as pd

# ──────────────────────────────
# CONFIGURATION
# ──────────────────────────────
FILE_RAW = "products.xlsx"          # input Excel file
KEEP_ONLY_WATER_T = False           # set True to filter برند == 'منبع آب'

# Column names (edit if your headers are different)
COL_CODE      = "کد محصول"          # A
COL_BRAND     = "برند"              # B
COL_TYPE      = "نوع"               # C
COL_CATEGORY = "دسته بندی"
COL_CAPACITY  = "لیتراژ"            # D
COL_DESC      = "توضیحات"           # E
COL_LENGTH    = "طول"               # F
COL_WIDTH     = "عرض"               # G
COL_HEIGHT    = "ارتفاع"            # H
COL_DIAMETER  = "قطر"               # I
COL_PRICE     = "قیمت به تومان"      # J

# ──────────────────────────────
# 1) LOAD + optional filter
# ──────────────────────────────
df = pd.read_excel(FILE_RAW)
if KEEP_ONLY_WATER_T:
    df = df[df[COL_BRAND] == "منبع آب"].copy()

# ──────────────────────────────
# 2) SPLIT by diameter
# ──────────────────────────────
with_diam     = df[df[COL_DIAMETER].notna()].copy()
without_diam  = df[df[COL_DIAMETER].isna()].copy()

# ──────────────────────────────
# 3) MERGE logic (Type + Capacity)
# ──────────────────────────────
group_cols = [COL_TYPE, COL_CAPACITY]
all_merged_rows = []
current_id = 1

for part_df, has_diameter in [(with_diam, True), (without_diam, False)]:
    for _, g in part_df.groupby(group_cols, sort=False):
        g = g.sort_index()  # preserve row order

        all_merged_rows.append({
            "ID"         : current_id,
            "SKUs"       : ", ".join(g[COL_CODE].astype(str)),
            "Brands"     : ", ".join(g[COL_BRAND].astype(str)),
            "Descs"      : ", ".join(g[COL_DESC].fillna("").astype(str)),
            COL_TYPE     : g.iloc[0][COL_TYPE],
            COL_CAPACITY : g.iloc[0][COL_CAPACITY],
            "Lengths"    : ", ".join(g[COL_LENGTH].fillna("").astype(str)),
            "Widths"     : ", ".join(g[COL_WIDTH].fillna("").astype(str)),
            "Heights"    : ", ".join(g[COL_HEIGHT].fillna("").astype(str)),
            "Diameters"  : ", ".join(g[COL_DIAMETER].fillna("").astype(str)) if has_diameter else "",
            "Prices"     : ", ".join(g[COL_PRICE].fillna("").astype(str)),
        })
        current_id += 1

merged = pd.DataFrame(all_merged_rows)

# ──────────────────────────────
# 4) Build parent + child rows for All Importer
# ──────────────────────────────
def assign_categories(row):
    base = "منبع آب"

    if row["نوع"] == "منبع آب":
        return base
    elif row["نوع"] == "کم جا":
        return f"{base} > کم جا"
    elif row["نوع"] == "کم جا رنگی":
        return f"{base} > کم جا > رنگی"
    elif row["نوع"] == "آسان رو":
        return f"{base} > آسان رو"
    elif row["نوع"] == "افقی":
        return f"{base} > افقی"
    elif row["نوع"] == "انبساط":
        return f"{base} > انبساط"
    elif row["نوع"] == "انبساط تک لایه آبی":
        return f"{base} > انبساط > تک لایه آبی"
    elif row["نوع"] == "بیضی":
        return f"{base} > بیضی"
    elif row["نوع"] == "زیر کامیونی":
        return f"{base} > زیر کامیونی"
    elif row["نوع"] == "زیرپله":
        return f"{base} > زیرپله"
    elif row["نوع"] == "سپراتش":
        return f"{base} > سپراتش"
    elif row["نوع"] == "عمودی":
        return f"{base} > عمودی"
    elif row["نوع"] == "قیفی":
        return f"{base} > قیفی"
    elif row["نوع"] == "مکعبی" or row["نوع"] == "مکعب افقی":
        return f"{base} > مکعب > افقی"
    elif row["نوع"] == "مکعب عمودی":
        return f"{base} > مکعب > عمودی"
    elif row["نوع"] == "نیسانی":
        return f"{base} > نیسانی"
    else:
        return f"{base} > بدون دسته‌بندی"


rows_out = []
for _, row in merged.iterrows():
    parent_sku = f"P{int(row['ID'])}"
    base_name = f"{row[COL_TYPE]} {row[COL_CAPACITY]}"

    # Parent row
    parent_row = {
        "SKU": parent_sku,
        "Parent": "",
        "Name": base_name,
        "Short description": "",
        "description": "",
        "litrage": row[COL_CAPACITY],
        "length": "",
        "width": "",
        "height": "",
        "diameter": "",
        "brand": "",
        "desc": "",
        "price": "",
    }

    rows_out.append(parent_row)

    # Split all list columns (children)
    skus      = [x.strip() for x in str(row["SKUs"]).split(",")]
    brands    = [x.strip() for x in str(row["Brands"]).split(",")]
    descs     = [x.strip() for x in str(row["Descs"]).split(",")]
    lengths   = [x.strip() for x in str(row["Lengths"]).split(",")]
    widths    = [x.strip() for x in str(row["Widths"]).split(",")]
    heights   = [x.strip() for x in str(row["Heights"]).split(",")]
    diameters = [x.strip() for x in str(row["Diameters"]).split(",")] if row["Diameters"] else ["" for _ in skus]
    prices    = [x.strip() for x in str(row["Prices"]).split(",")]

    max_len = max(len(skus), len(brands), len(descs), len(lengths), len(widths), len(heights), len(diameters), len(prices))

    # Pad all to same length
    def pad(lst): return lst + [""] * (max_len - len(lst))
    skus, brands, descs = pad(skus), pad(brands), pad(descs)
    lengths, widths, heights, diameters, prices = pad(lengths), pad(widths), pad(heights), pad(diameters), pad(prices)

    # Child rows
    for i in range(max_len):
        child_row = {
            "SKU": skus[i] if skus[i] else f"{parent_sku}-{i+1}",
            "Parent": parent_sku,
            "Name": f"{base_name} - {brands[i]} - {descs[i]}",
            "Short description": "",
            "description": "",
            "litrage": row[COL_CAPACITY],
            "length": lengths[i],
            "width": widths[i],
            "height": heights[i],
            "diameter": diameters[i],
            "brand": brands[i],
            "desc": descs[i],
            "price": prices[i],
            "categories": assign_categories(row),
        }

        rows_out.append(child_row)

# ──────────────────────────────
# 5) Output for All Importer (Excel and CSV)
# ──────────────────────────────
out_df = pd.DataFrame(rows_out)
out_df.to_excel("all_importer_products.xlsx", index=False, engine="openpyxl")
out_df.to_csv("all_importer_products.csv", index=False, encoding="utf-8-sig")

print("✅ All Importer format file written: all_importer_products.xlsx / .csv")
