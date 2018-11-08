# * coding:utf-8 *
# Author    : Administrator
# Createtime: 10/15/2018
import xlrd
import csv, json, os
import shutil

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def open_csv(file='C:\\Users\\Administrator\\PycharmProjects\\tool_2\\CSV\\AD_1_INLINE_TRAP4_Dual_V1_2018-09-15.csv'):
    header = []
    content = []
    line = 0
    csv_reader = csv.reader(open(file))
    for row in csv_reader:
        line = line + 1
        if line == 2:
            header = row
        if(line >= 8):
            content.append(row)
    return header, content

def excel_table_byname(file=u'C:\\Users\\Administrator\\PycharmProjects\\tool_2\\testItemList\\Tester_Spectram1011_.xlsx', colnameindex=0, by_name=u'Spectrum Item list'):  # 修改自己路径
    data = open_excel(file)
    table = data.sheet_by_name(by_name)  # 获得表格
    nrows = table.nrows  # 拿到总共行数
    colnames = table.row_values(colnameindex)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']
    list = []
    for rownum in range(1, nrows):  # 也就是从Excel第二行开始，第一行表头不算
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]  # 表头与数据对应
            list.append(app)
    return list

def main(file):
    result = []
    item = []
    X = []
    count = 0
    tables = excel_table_byname(file)
    for row in tables:
        if row['Item'] != '':
            item.append(row['Item'])
    for i in item:
        count = count + 1
        for row in tables:
            if i in row['X']:
                X.append(row['X'])
        result.append({'count': count, 'item': i, 'X': X})
        X = []
    return result

def get_chart_data(excel, csv_name, csv_path, config, overlay):
    try:
        x = []
        results = main(excel)
        headers, contents = open_csv(csv_path)
        serie = []
        location = []
        l = []
        m = []
        data = []
        series = []
        print(len(headers))
        for result in results:
            line = 0
            for header in headers:
                line = line + 1
                if header in result['X']:
                    print(header + "|" + str(line))
                    x.append(header.split('@')[1])
                    location.append(line)
            l.append({'item': result['item'], 'location': location, 'x': x})
            location = []
            x = []
        for item in l:
            for content in contents:
                for loca in item['location']:
                    if content[loca] == 'N/A':
                        data.append('null')
                    else:
                        data.append(float(content[loca - 1]))
                serie.append({'name': content[0], 'data': data})
                data = []
            series.append({'csv': csv_name, 'config': config, 'overlay': overlay, 'name': item['item'], 'data': serie,
                           'x': item['x']})
            serie = []
    except Exception as e:
        print(str(e))
    return series

def create_csv_folder(csv_path, root_path):
    list = os.listdir(csv_path)
    for item in list:
        location = os.path.join(root_path, item.split('.')[0])
        if os.path.exists(location) is False:
            os.makedirs(location)

def deleteFile(file_name):
    try:
        path = os.path.join(os.getcwd(), "CSV", "uploads", file_name)
        os.remove(path)
        result = {'state': 'success'}
    except Exception as e:
        print(str(e))
        result = {'state': 'error'}
    return result

def clearUploadedData(type=False):
    try:
        upload_csv_path = os.path.join(os.getcwd(), "CSV", "uploads")
        create_json_path = os.path.join(os.getcwd(), "utils", "phantomJS", "JSON")
        create_png_path = os.path.join(os.getcwd(), "PNG")

        if type:
            shutil.rmtree(upload_csv_path)
            os.mkdir(upload_csv_path)

        shutil.rmtree(create_json_path)
        os.mkdir(create_json_path)

        shutil.rmtree(create_png_path)
        os.mkdir(create_png_path)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    get_chart_data('C:\\Users\\Administrator\\PycharmProjects\\tool_2\\testItemList\\Tester_Spectram1011_.xlsx', 'C:\\Users\\Administrator\\PycharmProjects\\tool_2\\CSV\\AD_1_INLINE_TRAP4_Dual_V1_2018-09-15.csv')





