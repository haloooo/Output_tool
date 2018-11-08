from flask import Flask, render_template, request, Response, send_from_directory, redirect, url_for
import os, json
from werkzeug.utils import secure_filename
from utils import FileHelper, PhantomjsHelper

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def go_index_1():
    # file_location = os.path.join(os.path.dirname(__file__), 'CSV\\uploads')
    # del_file(file_location)
    FileHelper.clearUploadedData(True)
    return render_template('index.html')

@app.route('/go_index')
def go_index_2():
    # file_location = os.path.join(os.path.dirname(__file__), 'CSV\\uploads')
    # del_file(file_location)
    FileHelper.clearUploadedData(True)
    return render_template('index.html')

@app.route('/go_config')
def go_config():
    spectrum = request.args.get('spectrum')
    file_location = os.path.join(os.path.dirname(__file__), 'CSV\\uploads')
    png_location = os.path.join(os.path.dirname(__file__), 'PNG')
    FileHelper.create_csv_folder(file_location, png_location)
    return render_template('config.html',spectrum=spectrum, file_location=file_location)

@app.route('/get_item_list')
def get_item_list():
    path = os.path.join(os.getcwd(),'testItemList')
    result = getFilesByPath(path)
    jsonstr = json.dumps(result)
    return jsonstr

def getFilesByPath(path):
    result = []
    fs = os.listdir(path)
    for f in fs:
        tmp_path = os.path.join(path, f)
        print(tmp_path)
        result.append(f)
    return result

def getFilesByPath_json(path):
    result = []
    fs = os.listdir(path)
    for f in fs:
        tmp_path = os.path.join(path, f)
        print(tmp_path)
        result.append({'file_name':f, 'file_path':tmp_path, 'config':'', 'overlay':''})
    return result

def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/upload_csv', methods=['POST', 'GET'])
def upload_csv():
    try:
        if request.method == 'POST':
            for item in request.files:
                file_type = item.split('.')[1]
                if(file_type.lower() != 'csv'):
                    result = {'state': 'fail','msg':'please choose CSV file to upload'}
                    jsonstr = json.dumps(result)
                    return jsonstr
                f = request.files[item]
                basepath = os.path.dirname(__file__)  # 当前文件所在路径
                upload_path = os.path.join(basepath, 'CSV\\uploads',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
                f.save(upload_path)
        result = {'state': 'success'}
    except BaseException as exp:
        result = {'state': 'error'}
    jsonstr = json.dumps(result)
    return jsonstr

@app.route('/upload_xlsx', methods=['POST', 'GET'])
def upload_xlsx():
    try:
        if request.method == 'POST':
            for item in request.files:
                f = request.files[item]
                basepath = os.path.dirname(__file__)  # 当前文件所在路径
                upload_path = os.path.join(basepath, 'testItemList',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
                f.save(upload_path)
        result = {'state': 'success'}
    except BaseException as exp:
        result = {'state': 'error'}
    jsonstr = json.dumps(result)
    return jsonstr

@app.route('/upload_file')
def upload_file():
    file_location = request.args.get('file_location')
    result = getFilesByPath(file_location)
    jsonstr = json.dumps(result)
    return jsonstr

@app.route('/getCSV')
def getCSV():
    spectrum = request.args.get('spectrum')
    # file_location = request.args.get('file_location')
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    file_location = os.path.join(basepath, 'CSV\\uploads')
    result = getFilesByPath_json(file_location)
    jsonstr = json.dumps(result)
    return jsonstr

@app.route('/make_chart')
def make_chart():
    try:
        result = []
        data = json.loads(request.args.get('data'))
        spectrum = request.args.get('spectrum')
        path = os.path.join(os.path.join(os.getcwd(), 'testItemList'), spectrum)
        for item in data:
            result.append(FileHelper.get_chart_data(path, item['file_name'], item['file_path'], item['config'], item['overlay']))
        for index_1 in result:
            count = 0
            for index_2 in index_1:
                count = count + 1
                # if count == 8:
                #     config = index_2['config']
                #     overlay = index_2['overlay']
                #     csv_name = index_2['csv']
                #     name = index_2['name']
                #     categories = index_2['x']
                #     series = index_2['data']
                #     PhantomjsHelper.process_json(csv_name, name, categories, series, config, overlay)

                config = index_2['config']
                overlay = index_2['overlay']
                csv_name = index_2['csv']
                name = index_2['name']
                categories = index_2['x']
                series = index_2['data']
                PhantomjsHelper.process_json(csv_name, name, categories, series, config, overlay)
        png_zip = PhantomjsHelper.createPNG()
        result = {'state': 'success','png_zip': png_zip}
    except BaseException as exp:
        result = {'state': 'error'}
    jsonstr = json.dumps(result)
    return jsonstr

@app.route("/download/<filepath>", methods=['GET'])
def download_file(filepath):
    # 此处的filepath是文件的路径，但是文件必须存储在static文件夹下， 比如images\test.jpg
    return app.send_static_file(filepath)

@app.route("/deleteFile", methods=['GET'])
def deleteFile():
    file_name = request.args.get('file_name')
    result = FileHelper.deleteFile(file_name)
    jsonstr = json.dumps(result)
    return jsonstr

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True, threaded=True)
