from mylib import get_input, find_fresh_id, sum_merged_ranges



def main():

    # fname = 'ex.txt'
    fname = 'in.txt'

    range_data, ids = get_input(fname)

    find_fresh_id(range_data, ids)

    sum_merged_ranges(range_data)
    
if __name__ == "__main__":
    main()