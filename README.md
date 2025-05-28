# 🛠️ Product Merger & All Importer Formatter
![alt text](https://s6.uupload.ir/files/chatgpt_image_may_28,_2025,_05_38_39_pm_jkzi.png "Logo")
This Python project automates the **merging, formatting, and exporting** of product data for WordPress/WooCommerce **All Importer** tools.

It takes an initial raw Excel file (e.g., `products.xlsx`), processes it fully in one run, and outputs:
✅ **Merged master list** of parent + child products
✅ **All Importer–ready files** (`.xlsx` + `.csv`) with:

* Parent/Child structure
* Clean SKU mapping
* Length, width, height, diameter, capacity (لیتریژ)
* Prices, brands, descriptions
* Automatically generated **category paths** matching your site’s category tree

---

## 📦 Features

* 💾 One script handles:

  * Splitting by presence of diameter
  * Grouping products by نوع (type) + لیتراژ (capacity)
  * Building clean parent-child hierarchies
  * Generating unique SKUs for parents and variations
  * Padding aligned lists for All Importer compatibility
  * Assigning hierarchical Persian categories like:

    ```
    منبع آب > کم جا > رنگی
    ```

* 📤 Outputs:

  * `all_importer_products.xlsx`
  * `all_importer_products.csv`

* 🏷 Category mapping is fully automated based on product type.

---

## 📁 Input

You must provide:

```
products.xlsx
```

This Excel file should have at minimum:

* کد محصول (product code)
* برند (brand)
* نوع (type)
* لیتراژ (capacity)
* توضیحات (description)
* طول (length)
* عرض (width)
* ارتفاع (height)
* قطر (diameter)
* قیمت به تومان (price)

---

## 🏷 Category Structure

The script uses this category hierarchy:

```
منبع آب > [subtype]
```

For example:

* نوع == کم جا → منبع آب > کم جا
* نوع == کم جا رنگی → منبع آب > کم جا > رنگی
* نوع == انبساط تک لایه آبی → منبع آب > انبساط > تک لایه آبی

If the type is unknown, it defaults to:

```
منبع آب > بدون دسته‌بندی
```

You can edit the `assign_categories` function to change or expand the mappings.

---

## 🚀 How to Run

1️⃣ Install required libraries:

```bash
pip install pandas openpyxl
```

2️⃣ Run the script:

```bash
python your_script.py
```

3️⃣ Check the output files:

* `all_importer_products.xlsx`
* `all_importer_products.csv`

---

## 🛡 Notes

* The script assumes Persian headers; adjust the column names at the top if needed.
* SKU generation is customizable — currently uses parent ID + variation index if no direct code is provided.
* Category mappings follow the site category structure you provided.

---

## ✨ Contributing

Feel free to open issues or pull requests if you:

* Add more category mappings
* Improve the script’s flexibility
* Expand it for other WooCommerce importers

---

## 📜 License

MIT License — free to use and modify.
