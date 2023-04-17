import math


def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    # Check the integral list len if the list is lower than quantity call
    if len(page_range) <= qty_pages:
        return page_range

    # Create the pagination parametrization based on data entry
    middle = math.ceil(qty_pages / 2)
    start = 0
    if current_page > page_range[-1] - middle:
        # Case are in the last pages
        start = page_range[-1] - qty_pages
    elif current_page >= middle:
        # Case are in the initial pages
        start = current_page - middle
    stop = start + qty_pages
    return page_range[start:stop]
