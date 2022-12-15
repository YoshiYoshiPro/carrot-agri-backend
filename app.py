from flask import Flask, jsonify, request
import os
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# CSVファイルから情報を読み込む（仮）
flask_conf_file = os.path.join(os.getcwd(), 'conf', 'flask_conf.cfg')
mail_file = os.path.join(os.getcwd(), 'data', 'personal_info.csv')
app.config.from_pyfile(flask_conf_file)

# MySQL接続
mysql = MySQL()
mysql.init_app(app)

@app.route('/', methods=["GET"])
def index():
    result_dict = {}
    mail_address_list = []
    target_prefecture = request.args.get('pref')

    with open(mail_file, 'r') as inf:
        for low_num, line in enumerate(inf):
            if low_num == 0:  # header
                continue
            line = line.rstrip()
            vals = line.split(',')
            mail_add, sex, age, name, prefecture = vals
            if prefecture == target_prefecture:
                mail_address_list.append(mail_add)

    result_dict['mail_address_list'] = mail_address_list
    return jsonify(result_dict)

if __name__ == '__main__':
    app.run()
