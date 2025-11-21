import csv

# README!
# 1. First make sure that TEMPLATE_CODELIST is manually (!) filled by you and pasted into beggining of the change set.
#    Remember that script does not automatize this part, you need to do it manually.
# 2. Then edit input.csv file, add row for every codelist_item that should be under that CODELIST.
# 3. Then run this script, paste generated content UNDER previously pasted CODELIST part.Check previous MRs if necessary to verify the structure.

# -------------------------------
# TEMPLATES
# -------------------------------
TEMPLATE_CODELIST = """
        <!--   codelist     -->
        <insert tableName="codelist">
            <column name="codelist_key" value="XXXXXXXXXXXXXXXXXXXXXXXXX"/>
            <column name="codelist_type"/>
            <column name="owner_cl" value="CUSTOM"/>
        </insert>

        <insert tableName="codelist_label">
            <column name="description" value=""XXXXXXXXXXXXXXXXXXXXXXXXX"" />
            <column name="codelist_id" valueComputed="(select id from codelist where codelist_key = '"XXXXXXXXXXXXXXXXXXXXXXXXX"')" />
            <column name="language_cl" value="EN" />
        </insert>

        <insert tableName="codelist_label">
            <column name="description" value=""XXXXXXXXXXXXXXXXXXXXXXXXX"" />
            <column name="codelist_id" valueComputed="(select id from codelist where codelist_key = '"XXXXXXXXXXXXXXXXXXXXXXXXX"')" />
            <column name="language_cl" value="LT" />
        </insert>

        <insert tableName="codelist_category">
            <column name="codelist_id" valueComputed="(select id from codelist where codelist_key = '"XXXXXXXXXXXXXXXXXXXXXXXXX"')" />
            <column name="category_code" value=""XXXXXXXXXXXXXXXXXXXXXXXXX"" />
        </insert>
"""

TEMPLATE_ITEM = """
        <!--   {{item_code}} --> 
        <insert tableName="codelist_item">
            <column name="item_code" value="{{item_code}}"/>
            <column name="codelist_id" valueComputed="(select id from codelist where codelist_key = '{{codelist}}')"/> 
            <column name="owner_cl" value="CUSTOM"/>
            <column name="valid_from" value="1900-01-01 01:00:00.000 +0200"/>
            <column name="valid_to" valueComputed="NULL"/>
            <column name="sorting" value="{{sorting}}"/>
        </insert>

        <insert tableName="codelist_item_label">
            <column name="item_id" valueComputed="(
                select ci.id from codelist_item ci
                join codelist c on ci.codelist_id = c.id
                where ci.item_code = '{{item_code}}' and c.codelist_key = '{{codelist}}'
            )"/>
            <column name="language_cl" value="EN"/>
            <column name="description" value="{{EN_description}}"/> 
        </insert>

        <insert tableName="codelist_item_label">
            <column name="item_id" valueComputed="(
                select ci.id from codelist_item ci
                join codelist c on ci.codelist_id = c.id
                where ci.item_code = '{{item_code}}' and c.codelist_key = '{{codelist}}'
            )"/>
            <column name="language_cl" value="LT"/>
            <column name="description" value="{{LT_description}}"/> 
        </insert>
"""

# -------------------------------
# CSV FILE PATH
# -------------------------------
CSV_PATH = "resources/data/input.csv"   # <-- enter path to CSV file, it must be encoded in UTF-8, and semicolon-separated (;)

# -------------------------------
# PROCESS CSV
# -------------------------------
final_script = ""

with open(CSV_PATH, encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=';')
    print(reader.fieldnames)
    reader.fieldnames = [name.strip().replace('\ufeff','') for name in reader.fieldnames]  #\ufeff is some weird sequence in case you have utf-8-sig file
    for row in reader:
        current_row = TEMPLATE_ITEM
        current_row = current_row.replace("{{item_code}}", row["item_code"])
        current_row = current_row.replace("{{codelist}}", row["codelist"])
        current_row = current_row.replace("{{EN_description}}", row["EN_description"])
        current_row = current_row.replace("{{LT_description}}", row["LT_description"])
        current_row = current_row.replace("{{sorting}}", row["sorting"])

        final_script += current_row + "\n"


# -------------------------------
# PRINT RESULT
# -------------------------------
print(final_script)