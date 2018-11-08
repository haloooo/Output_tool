# * coding:utf-8 *
# Author    : Administrator
# Createtime: 10/17/2018

import json, os, uuid

from utils import FileHelper, ZipFileHelper


def process_json(csv_name, output_json_filename, categories, series, config, overlay):
    input_json_file = os.path.join(os.getcwd(), 'utils', 'phantomJS','content.json')
    csv_folder = csv_name.split('.')[0]
    csv_folder_path = os.path.join(os.getcwd(), 'utils', 'phantomJS','JSON',csv_folder)
    if os.path.exists(csv_folder_path) is False:
        os.makedirs(csv_folder_path)
    output_json_file = os.path.join(csv_folder_path,output_json_filename+'.json')
    # if not os.path.exists(output_json_file):
    #     os.makedirs(output_json_file)
    file_in = open(input_json_file,mode='r',encoding='utf-8')
    file_out = open(output_json_file, "w")
    # load数据到变量json_data
    json_data = json.load(file_in)
    # 修改json中的数据
    json_data['xAxis']['categories'] = categories
    json_data['series'] = series
    json_data['title']['text'] = output_json_filename
    json_data['subtitle']['text'] = "Config " + config + ", Overlay" + overlay + "<br>" + output_json_filename + "(N=" + str(len(series)) + ")"
    print(json_data['xAxis']['categories'])

    # 将修改后的数据写回文件
    file_out.write(json.dumps(json_data))
    file_in.close()
    file_out.close()

def createPNG():
    phantomjs_path = os.path.join(os.getcwd(),'utils', 'phantomJS', 'phantomjs.exe')
    highcharts_convert_path = os.path.join(os.getcwd(),'utils', 'phantomJS', 'highcharts-convert.js')
    rootdir = os.path.join(os.getcwd(),'utils', 'phantomJS', 'JSON')
    list = os.listdir(rootdir)
    for i in range(0,len(list)):
        json_path = os.path.join(rootdir,list[i])
        json_list = os.listdir(json_path)
        for j in range(0,len(json_list)):
            json_file_path = os.path.join(json_path, json_list[j])
            png_path = os.path.join(os.getcwd(), 'PNG', list[i], json_list[j]) + '.png'
            command = phantomjs_path + " " + highcharts_convert_path + " -infile " + "\"" + json_file_path + "\"" + ' -outfile ' + "\"" + png_path + "\""
            os.system(command)
    png_zip = str(uuid.uuid1()) + '.zip'
    startdir = os.path.join(os.getcwd(),'PNG')
    file_news = os.path.join(os.getcwd(),'static',png_zip)
    ZipFileHelper.zip_ya(startdir, file_news)
    FileHelper.clearUploadedData()
    return png_zip

if __name__ == '__main__':
    # process_json("../jsonfile/mysql2hive_templet.json", "../jsonfile/mysql2hive_instance.json")
    # process_json('test')
    # output_json_file = os.path.join(os.getcwd(), 'phantomJS', 'JSON', 'test.json')
    # createPNG()
    # list = os.listdir('C:\\Users\\Administrator\\PycharmProjects\\tool_2\\utils\\phantomJS\\JSON')
    print(str(uuid.uuid4()) + '.zip')


