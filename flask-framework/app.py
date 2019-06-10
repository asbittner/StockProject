from flask import Flask, render_template, request, redirect
import pandas as pd
import bokeh.plotting as bk
import bokeh.embed as bke
import requests as rq
import simplejson as json

def get_data(ticker, month, year):
    req = rq.get('https://www.quandl.com/api/v3/datasets/WIKI/' + ticker + '/data.json?api_key=WWhbwTh6zX3RTBHsv6a-')
    j = req.json()
    df = pd.DataFrame(j['dataset_data']['data'], columns = j['dataset_data']['column_names'])
    df['DateList'] = df['Date'].str.split('-')
    df['Month'] = df['DateList'].map(lambda x: x[1])
    df['Day'] = df['DateList'].map(lambda x: int(x[2]))
    df['Year'] = df['DateList'].map(lambda x: x[0])
    df_yr = df[df['Year'] == year]
    return df_yr[df_yr['Month'] == month]

def plot_data(data):
    p = bk.figure()
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.line(data['Day'], data['Close'])
    return p


app = Flask(__name__)

@app.route('/stock_graph', methods = ['GET', 'POST'])
def graph_stock():
    if request.method == 'GET':
        return render_template('userinfo_stock.html')
    else:
        d = get_data(str(request.form['ticker']), str(request.form['month']), str(request.form['year']))
        plot = plot_data(d)
        script,div = bke.components(plot)
        return render_template('plot_stock.html', script = script, div = div)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507, debug = True)
