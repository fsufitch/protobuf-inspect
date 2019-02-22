import base64, flask, glob, os, shlex, subprocess

PROTO_ROOT = os.getenv('PROTO_ROOT')
PROTO_FILES = glob.glob(os.getenv('PROTO_FILE'))
if not PROTO_FILES:
    raise RuntimeError(f"No proto files found at {os.getenv('PROTO_FILE')}")

app = flask.Flask(__name__)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def root():
    response = app.make_response("Try /<packagename.MessageName>")
    response.headers['Content-type'] = 'text/plain'
    return response

@app.route('/<messagetype>')
def message_ui(messagetype):
    return flask.send_file('static/index.html')

@app.route('/s/<path:path>')
def static_files(path):
    return flask.send_from_directory('static', path)

@app.route('/<messagetype>/decode', methods=['POST'])
def decode(messagetype):
    command = [
        'protoc',
        '-I', PROTO_ROOT,
        '--decode=' + messagetype,
        *PROTO_FILES,
    ]

    b64_data = flask.request.data
    pbuf_data = base64.b64decode(b64_data.decode())

    proc = subprocess.Popen(command, 
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    stdout, stderr = proc.communicate(pbuf_data)
    returncode = proc.wait()

    if returncode == 0:
        return flask.jsonify({
            'command': command,
            'error': '',
            'text': stdout.decode(),
        })
    else:
        text_command = ' '.join([shlex.quote(x) for x in command])
        return flask.jsonify({
            'command': command,
            'error': f"Command `{text_command}` returned code {returncode}",
            'text': f"STDOUT:\n{stdout.decode()}\n\nSTDERR:\n{stderr.decode()}",
        })

@app.route('/<messagetype>/encode', methods=['POST'])
def encode(messagetype):
    command = [
        'protoc',
        '-I', PROTO_ROOT,
        '--encode=' + messagetype,
        *PROTO_FILES,
    ]

    pbuf_text_data = flask.request.data

    proc = subprocess.Popen(command, 
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    stdout, stderr = proc.communicate(pbuf_text_data)
    returncode = proc.wait()

    if returncode == 0:
        response_data = base64.b64encode(stdout).decode()
        print(response_data)
        return flask.jsonify({
            'command': command,
            'error': '',
            'data': response_data,
        })
    else:
        text_command = ' '.join([shlex.quote(x) for x in command])
        return flask.jsonify({
            'command': command,
            'error': f"Command `{text_command}` returned code {returncode}",
            'text': f"STDERR:\n{stderr.decode()}",
        })