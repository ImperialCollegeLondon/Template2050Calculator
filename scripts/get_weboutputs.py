import json
import sys

from openpyxl import load_workbook


def get_cells(ref, workbook):
    sheet, cells = ref.split("!")
    return workbook[sheet][cells]


def table_to_dict(table):
    keys = [cell.value for cell in table[0]]
    table_dict = {}
    for row in table[1:]:
        for key, col in zip(keys, row):
            if key is None:
                continue
            table_dict.setdefault(key, []).append(col.value)
    return table_dict


def dict_from_range(range_name, wb):
    return table_to_dict(get_cells(wb.defined_names[range_name].attr_text, wb))


def check_tooltips(tooltips):
    for row in tooltips:
        for cell in row:
            if cell.value is None:
                raise ValueError(f"Found blank tooltip in {cell}")


def get_weboutputs(wb):
    summary_table = dict_from_range("outputs_summary_table", wb)
    example_pathways = dict_from_range("output.lever.example.ambition", wb)

    lever_groups = [
        get_cells(dn.attr_text, wb)
        for dn in wb.defined_names.definedName
        if "output.lever.group" in dn.name
    ]

    tooltips = list(
        get_cells(wb.defined_names["output.lever.descriptions"].attr_text, wb)
    )
    check_tooltips(tooltips)

    output_lever_names_grouped = {}
    for group in lever_groups:
        group_name = group[0][0].value
        output_lever_names_grouped[group_name] = {"names": [], "tooltips": []}
        for row in group:
            output_lever_names_grouped[group_name]["names"].append(row[1].value)
            output_lever_names_grouped[group_name]["tooltips"].append(
                [str(cell.value) for cell in tooltips.pop(0)]
            )

    return dict(
        weboutputs_summary_table=summary_table,
        example_pathways=example_pathways,
        output_lever_names_grouped=output_lever_names_grouped,
    )


if __name__ == "__main__":
    wb = load_workbook(
        filename=sys.argv[1], data_only=True, read_only=True, keep_vba=False
    )

    with open("web_outputs.json", "w") as outfile:
        json.dump(
            get_weboutputs(wb),
            outfile,
            indent=4,
        )
