

def get_input(fname):
    with open(fname, 'r') as f:
        # data = f.read().strip().splitlines()
        data = f.read()

        # split on double newlines
        data = data.split('\n\n')
        ## assert len(data) == 2
        assert len(data) == 2, f"Expected 2 sections, got {len(data)}"
        range_data, ids = data
        range_data = range_data.strip().splitlines()
        range_data = [list(map(int, line.split('-'))) for line in range_data]
        ids = ids.strip().splitlines()
        ids = [int(x) for x in ids]

    return range_data, ids

def find_fresh_id(range_data, ids):

    # range data is a list of [start, end] pairs of fresh ID ranges
    # ids is a list of all IDs
    # Create a set of all fresh IDs

    fresh_set = set()

    for id in ids:
        for start, end in range_data:
            if start <= id <= end:
                fresh_set.add(id)
                # print(f"ID {id} is fresh in range {start}-{end}")
                break
    
    # report number of fresh IDs
    print(f"Number of fresh IDs: {len(fresh_set)}")

    return None

def sum_merged_ranges(range_data):

    # range data is a list of [start, end] pairs of fresh ID ranges
    # some ranges may overlap
    # create list of ranges that cover all fresh IDs without overlap
    merged_ranges = []
    for start, end in sorted(range_data):
        if not merged_ranges or merged_ranges[-1][1] < start - 1:
            merged_ranges.append([start, end])
        else:
            merged_ranges[-1][1] = max(merged_ranges[-1][1], end)

    # sum up total number of fresh IDs
    total_fresh = sum(end - start + 1 for start, end in merged_ranges)
    print(f"Total number of fresh IDs: {total_fresh}")
    
    return None