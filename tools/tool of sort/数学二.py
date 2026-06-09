base_2025 = [936, 934, 935, 930, 931, 933, 932, 915, 916, 924, 923, 921, 922, 917, 918, 920, 919, 928, 929, 926, 925, 927]
base_2020 = [1047, 1045, 1046, 1041, 1042, 1044, 1043, 1025, 1026, 1034, 1033, 1031, 1032, 1027, 1028, 1030, 1029, 1039, 1040, 1036, 1035, 1037, 1038]
def generate_year_data(year):
    range_mapping_2009_2014 = {
        2015: (1756,1778),
        2014: (1733,1755),
        2013: (1710,1732),
        2012: (1687,1709),
        2011: (1664,1686),
        2010: (1641,1663),
        2009: (1618,1640)
    }

    if 2009 <= year <= 2014:
        start, end = range_mapping_2009_2014[year]
        return list(range(start,end+1))
    if 2015 <= year<= 2020:
        offset1 = 23*(year-2015)
        return [num + offset1 for num in base_2020]
    elif 2021 <= year <= 2025:
        offset2 = 22*(year-2025)
        return [num - offset2 for num in base_2025]
    return "仅支持 2009–2025 年数据生成"
if __name__ == "__main__":
    for year in range(2009, 2026):
        data = generate_year_data(year)
        print(f"{year}年（{len(data)}）")
        print(".png,".join(map(str, data))+".png" + "\n")

