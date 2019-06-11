from flask import Flask, render_template, request, redirect
import pandas as pd
import bokeh.plotting as bk
import bokeh.embed as bke
import quandl as qd

qd.ApiConfig.api_key = 'WWhbwTh6zX3RTBHsv6a-'

def get_data(ticker, month, year):
    df = qd.get('WIKI/' + ticker)
    df['Date'] = df.index
    df['Month'] = df['Date'].map(lambda x: x.month)
    df['Day'] = df['Date'].map(lambda x: x.day)
    df['Year'] = df['Date'].map(lambda x: x.year)
    df_yr = df[df['Year'] == int(year)]
    return df_yr[df_yr['Month'] == int(month)]

def plot_data(data, ticker):
    p = bk.figure(x_axis_type = 'datetime')
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.line(data['Date'], data['Open'], legend = ticker + ' Open', line_color="green")
    p.line(data['Date'], data['Close'], legend = ticker + ' Close')
    return p


app = Flask(__name__)

@app.route('/stock_graph', methods = ['GET', 'POST'])
def graph_stock():
    if request.method == 'GET':
        return render_template('userinfo_stock.html')
    else:
        d = get_data(str(request.form['ticker']), str(request.form['month']), str(request.form['year']))
        plot = plot_data(d, str(request.form['ticker']))
        script,div = bke.components(plot)
        return render_template('plot_stock.html', script = script, div = div)

@app.route('/')
def index():
  return render_template('userinfo_stock.html')

if __name__ == '__main__':
  app.run(port=33507, debug = True)
