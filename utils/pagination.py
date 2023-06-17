import math
from django.core.paginator import Paginator


def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    # Create the pagination parametrization based on data entry
    middle = math.ceil(qty_pages / 2)
    start = 0
    total_pages = len(page_range)

    # Check the integral list len if the list is lower than quantity call
    if total_pages <= qty_pages:
        pagination = page_range
        return {
            'pagination': pagination,
            'page_range': page_range,
            'qty_pages': qty_pages,
            'current_page': current_page,
            'total_pages': total_pages,
            'start': start,
            'first_out_of_range': False,
            'last_out_of_range': False,
        }
    # Check the correct ranges and apply on return
    if current_page > page_range[-1] - middle:
        # Case are in the last pages
        start = page_range[-1] - qty_pages
    elif current_page >= middle:
        # Case are in the initial pages
        start = current_page - middle
    stop = start + qty_pages
    # The list return
    pagination = page_range[start:stop]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start': start,
        'first_out_of_range': current_page > middle,
        'last_out_of_range': stop < total_pages,
    }

# Custom Pagination


def make_pagination(request, queryset, per_page=9, paginator_size=5):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        paginator_size,
        current_page,
    )

    return page_obj, pagination_range
