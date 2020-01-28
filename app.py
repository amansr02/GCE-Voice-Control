import sys
from flask import Flask, request, abort
from create_instance import main

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    print("webhook"); sys.stdout.flush()
    if request.method == 'POST':
        dictionary = dict(request.json)
        project = dictionary["project"]
        bucket = "gs://"+project+".appspot.com"
        instance_name = dictionary["name"]
        zone = dictionary["zone"]
        main(project,bucket,zone,instance_name)
        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run()
