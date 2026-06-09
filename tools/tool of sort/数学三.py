base_2025 = [1207, 1205, 1206, 1201, 1202, 1204, 1203, 1186, 1187, 1195, 1194, 1192, 1193, 1188, 1189, 1191, 1190, 1199, 1200, 1197, 1196, 1198]
base_2020 = [1318, 1316, 1317, 1312, 1313, 1315, 1314, 1296, 1297, 1305, 1304, 1302, 1303, 1298, 1299, 1301, 1300, 1310, 1311, 1307, 1306, 1308, 1309]
def generate_year_data(year):
    range_mapping_2009_2014 = {
        2015: (1917, 1939),
        2014: (1894, 1916),
        2013: (1871, 1893),
        2012: (1848, 1870),
        2011: (1825, 1847),
        2010: (1802, 1824),
        2009: (1779, 1801)
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
