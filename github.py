from flask import Flask, render_template, jsonify
import os, subprocess
from flask_apscheduler import APScheduler


app = Flask(__name__)
with app.app_context():
    scheduler = APScheduler()
    scheduler.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/github')
def github():
   return githubContribute()

@scheduler.task('interval', id='github_job', hours=8)
def githubContribute():
    print("running...")
    result = runShell("./run.sh")
    print(result)
    return jsonify({"code": 0})

# 执行脚本
def runShell(script):
    p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
    while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
        hasSuccess = p.wait() == 0
        re = p.stdout.readlines()  # 获取原始执行结果
        result = []
        for i in range(len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
            res = re[i].decode('utf-8').strip('\r\n')
            result.append(res)
        return "\n".join(result)
    

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0', port=8801, debug=True)
