from flask import Flask, render_template, jsonify
import analysis.base_1 as data
import analysis.base_2 as data2

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html', data=data.results, data2=data2.results)

@app.route('/data')
def get_data():
    return jsonify({'data': data.results, 'data2': data2.results})

if __name__ == '__main__':
    app.run(debug=True)
