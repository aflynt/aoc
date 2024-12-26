

def main():
    fnames = [
        "ex13.txt",
        "in13.txt",
    ]

    ms = read_machines(fnames[-1])
    print(f"{calc(ms, False):18,}")
    print(f"{calc(ms, True):18,}")


def is_close_to_whole(x, tol=0.001):

    xr = round(x)
    diff = abs(x - xr)
    is_ok = diff < tol
    if is_ok:
        return True
    else:
        return False


def read_machines(fname:str ):
    with open(fname, "r") as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]
    lines.append("")

    ms = []
    for line in lines:
        if line.startswith("Button A"):
            x = line
            _,x = line.split(": ")
            dxastr,dyastr = x.split(", ")
            dxa = int(dxastr.split("+")[-1])
            dya = int(dyastr.split("+")[-1])
        elif line.startswith("Button B"):
            x = line
            _,x = line.split(": ")
            dxastr,dyastr = x.split(", ")
            dxb = int(dxastr.split("+")[-1])
            dyb = int(dyastr.split("+")[-1])
        elif line.startswith("Prize"):
            x = line
            _,x = line.split(": ")
            dxastr,dyastr = x.split(", ")
            xf = int(dxastr.split("=")[-1])
            yf = int(dyastr.split("=")[-1])
        else:
            ms.append((dxa,dya, dxb,dyb, xf,yf))
    return ms


def calc(ms, is_p2=False):

    ans = 0
    for i,m in enumerate(ms):
        dxa,dya,dxb,dyb,xf,yf = m

        if is_p2:
            xf += 10000000000000
            yf += 10000000000000

        c = dxa - dya*dxb/dyb
        n = (xf - yf*dxb/dyb)/c
        m = (yf - n*dya)/dyb

        is_ok = 0 <= n and 0 <= m and is_close_to_whole(n) and is_close_to_whole(m)

        if is_ok:
            cost = 3*n + m
        else:
            cost = 0

        ans += cost
    return int(ans)

if __name__ == "__main__":
    main()
