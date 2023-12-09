
#str = open('example.txt','r').read()
str = open('input.txt','r').read()

glist = str.splitlines()


def get_game_nums(glist):
    game_nums = []
    for g in glist:
        game_str = g.split(':')[0]
        game_num = int(game_str.strip().split()[-1])
        game_nums.append(game_num)
    return game_nums

def get_game_sets(glist):
    sets = []
    for g in glist:
        set_str = g.split(':')[1]
        gset_strs = set_str.split(';')
        sets.append(gset_strs)

    return sets

gnums = get_game_nums(glist)
sets = get_game_sets(glist)


allgames_picksets = []

for game_set in sets:
    game_picks = []
    #print('#')
    for setstr in game_set:
        #print('-|'+setstr+'|')
        pick_list = setstr.split(',')
        pick_r = 0
        pick_g = 0
        pick_b = 0
        for pick in pick_list:
            cnt_str,cubetype = pick.strip().split()
            cubetype = cubetype.strip()
            cnt = int(cnt_str)
            if cubetype == 'red':
                pick_r = cnt
            elif cubetype == 'green':
                pick_g = cnt
            else:
                pick_b = cnt
        #print(f' <{pick_r} {pick_g} {pick_b}>')
        set_pick = (pick_r, pick_g, pick_b)
        game_picks.append(set_pick)
    allgames_picksets.append(game_picks)

bag_r,bag_g,bag_b = (12, 13, 14)

res = 0
for i,game_sets in enumerate(allgames_picksets):
    id = i+1
    okint = 1
    for game_set in game_sets:
        r,g,b = game_set
        dr = bag_r - r
        dg = bag_g - g
        db = bag_b - b
        is_ok_r = dr >= 0
        is_ok_g = dg >= 0
        is_ok_b = db >= 0
        oklist = [is_ok_r, is_ok_g, is_ok_b]
        set_ok = all(oklist)
        if not set_ok:
            okint = 0
    res += id*okint
    print(f'ID: {id}: OK: {okint} r: {res:2d}',game_sets)

