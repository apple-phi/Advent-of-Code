import itertools
import math
import collections

table = str.maketrans(
    {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
)

PacketData = collections.namedtuple(
    "PacketData", ["val", "len", "cum_version_num", "lst_vals"], defaults=[0, 0, 0, []]
)
PacketData.__add__ = lambda self, other: PacketData(
    self.val + other.val,
    self.len + other.len,
    self.cum_version_num + other.cum_version_num,
    self.lst_vals + other.lst_vals,
)

with open("i") as f:
    data = f.read().translate(table)


def literal_len(s: str) -> int:
    """Get the start index of the next literal packet."""
    return (s[6::5].index("0") + 1) * 5 + 6 if int(s) else math.inf


def parse_literal(s: str, version: int) -> PacketData:
    """Get the number encoded by a literal packet."""
    _s = s[6:]
    val = int(
        "".join(
            _s[i - 4 : i]
            for i in itertools.takewhile(
                lambda i: _s[i - 10] == "1" or i < 10,
                range(5, len(_s) + 1, 5),
            )
        )
        or "0",
        2,
    )
    return PacketData(val, literal_len(s), version, [val])


def parse_packet(s: str) -> PacketData:
    # print(s)
    if not s or not int(s) or len(s) < 7:
        return PacketData()
    p_version = int(s[:3], 2)
    p_type_id = s[3:6]
    if p_type_id == "100":
        # print(f"Lit    | {s} | {parse_literal(s,p_version)}")
        return parse_literal(s, p_version)
    length_type_id = s[6]
    if length_type_id == "0":
        total_length = int(s[7:22], 2)
        cumsum = PacketData()
        while cumsum.len < total_length:
            cumsum += parse_packet(s[22 + cumsum.len :])
        # print(
        #     f"Type 0 | {s} | {PacketData(cumsum.val, 22 + total_length, cumsum.cum_version_num + p_version)}"
        # )
        out = PacketData(
            cumsum.val,
            22 + total_length,
            cumsum.cum_version_num + p_version,
            cumsum.lst_vals,
        )
    elif length_type_id == "1":
        num_sub = int(s[7:18], 2)
        cumsum = PacketData()
        for _ in range(num_sub):
            cumsum += parse_packet(s[18 + cumsum.len :])
        # print(f"Type 0 | {s} | {cumsum + PacketData(0, 18, p_version)}")
        out = cumsum + PacketData(0, 18, p_version)
    # print(length_type_id, out)
    p_type_id = int(p_type_id, 2)
    if p_type_id == 0:
        val = out.val
    elif p_type_id == 1:
        val = math.prod(out.lst_vals)
    elif p_type_id == 2:
        val = min(out.lst_vals)
    elif p_type_id == 3:
        val = max(out.lst_vals)
    elif p_type_id == 5:
        val = out.lst_vals[0] > out.lst_vals[1]
    elif p_type_id == 6:
        val = out.lst_vals[0] < out.lst_vals[1]
    elif p_type_id == 7:
        val = out.lst_vals[0] == out.lst_vals[1]
    else:
        raise ValueError
    return PacketData(val, out.len, out.cum_version_num, [val])


print(parse_packet(data))
