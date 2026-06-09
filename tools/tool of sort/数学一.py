base_2025 = [665, 663, 664, 659, 660, 662, 661, 644, 645, 653,652, 650, 651, 646, 647, 649, 648, 657, 658, 655, 654, 656]
base_2020 = [776, 774, 775, 770, 771, 773, 772, 754, 755, 763, 762, 760, 761, 756, 757, 759, 758, 768, 769, 765, 764, 766, 767]
def generate_year_data(year):
    range_mapping_2009_2014 = {
        2015: (1595, 1617),
        2014: (1572, 1594),
        2013: (1549, 1571),
        2012: (1526, 1548),
        2011: (1503, 1525),
        2010: (1480, 1502),
        2009: (1457, 1479)
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
        print(".png,".join(map(str, data)) +".png"+ "\n")
