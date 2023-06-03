from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def generate_graphs(csv_data):
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')))

    # Plot a bar graph
    plt.figure()
    df.plot(kind='bar', x='Category', y='Value')
    plt.title('Bar Graph')
    plt.xlabel('Category')
    plt.ylabel('Value')
    bar_graph = get_image_base64()

    # Plot a line graph
    plt.figure()
    df.plot(kind='line', x='Category', y='Value')
    plt.title('Line Graph')
    plt.xlabel('Category')
    plt.ylabel('Value')
    line_graph = get_image_base64()

    # Plot a scatter plot
    plt.figure()
    df.plot(kind='scatter', x='Category', y='Value')
    plt.title('Scatter Plot')
    plt.xlabel('Category')
    plt.ylabel('Value')
    scatter_plot = get_image_base64()

    return bar_graph, line_graph, scatter_plot

def get_image_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return image_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csv_file = request.files['csv_file']
        if csv_file:
            csv_data = csv_file.read()
            bar_graph, line_graph, scatter_plot = generate_graphs(csv_data)
            return render_template('result.html', bar_graph=bar_graph, line_graph=line_graph, scatter_plot=scatter_plot)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
