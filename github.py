from flask import Flask, render_template, jsonify
import os, subprocess
import schedule

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/github/contribute")
def githubContribute():
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
    
schedule.every(3).minutes.do(githubContribute)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8801, debug=True)
    while True:
        schedule.run_pending()
        time.sleep(1)


