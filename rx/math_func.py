def median(data):
    """
    Calculate the median of a list of numbers.
    Works for odd/even length lists.
    Raises ValueError if list is empty.
    """
    if not data:
        raise ValueError("median() arg is an empty sequence")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2

    if n % 2 == 1:
        # Odd number of elements
        return sorted_data[mid]
    else:
        # Even number of elements: average the two middle values
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2