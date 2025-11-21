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
            <column name="codelist_key" value="LT_TYPES_OF_PERSONS"/>
            <column name="codelist_type"/>
            <column name="owner_cl" value="CUSTOM"/>
        </insert>

        <insert tableName="codelist_label">
            <column name="description" value="Person types" />
            <column name="codelist_id" valueComputed="(select id from codelist where codelist_key = 'LT_TYPES_OF_PERSONS')" />
            <column name="language_cl" value="EN" />
        </insert>

        <insert tableName="codelist_label">
            <column name="description" value="Asmenų tipai" />
            <column name="codelist_id" valueComputed="(select id from codelist where codelist_key = 'LT_TYPES_OF_PERSONS')" />
            <column name="language_cl" value="LT" />
        </insert>

        <insert tableName="codelist_category">
            <column name="codelist_id" valueComputed="(select id from codelist where codelist_key = 'LT_TYPES_OF_PERSONS')" />
            <column name="category_code" value="REGISTRATION" />
        </insert>
"""

TEMPLATE_ITEM = """
        <!--   {{ID_number}} --> 
        <insert tableName="codelist_item">
            <column name="item_code" value="{{ID_number}}"/>
            <column name="codelist_id" valueComputed="(select id from codelist where codelist_key = '{{codelist}}')"/> 
            <column name="owner_cl" value="CUSTOM"/>
            <column name="valid_from" value="1900-01-01 01:00:00.000 +0200"/>
            <column name="valid_to" valueComputed="NULL"/>
        </insert>

        <insert tableName="codelist_item_label">
            <column name="item_id" valueComputed="(
                select ci.id from codelist_item ci
                join codelist c on ci.codelist_id = c.id
                where ci.item_code = '{{ID_number}}' and c.codelist_key = '{{codelist}}'
            )"/>
            <column name="language_cl" value="EN"/>
            <column name="description" value="{{EN_translation}}"/> 
        </insert>

        <insert tableName="codelist_item_label">
            <column name="item_id" valueComputed="(
                select ci.id from codelist_item ci
                join codelist c on ci.codelist_id = c.id
                where ci.item_code = '{{ID_number}}' and c.codelist_key = '{{codelist}}'
            )"/>
            <column name="language_cl" value="LT"/>
            <column name="description" value="{{LT_translation}}"/> 
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
        current_row = current_row.replace("{{ID_number}}", row["ID_number"])
        current_row = current_row.replace("{{codelist}}", row["codelist"])
        current_row = current_row.replace("{{EN_translation}}", row["EN_translation"])
        current_row = current_row.replace("{{LT_translation}}", row["LT_translation"])

        final_script += current_row + "\n"


# -------------------------------
# PRINT RESULT
# -------------------------------
print(final_script)