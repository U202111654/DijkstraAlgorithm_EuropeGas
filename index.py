from flask import Flask, render_template
import algorithm
app = Flask(__name__)

@app.route('/')
def home():
    g, airports_array, routes_array = algorithm.createGraph()
    paths = algorithm.findRoutes(g,airports_array,2789,3077)
    folium_map = algorithm.showMap(paths,airports_array,routes_array)
    #folium_map = algorithm.showMap([],[],[])
    #return folium_map._repr_html_()
    folium_map.save('templates/map.html')
    return render_template('index.html')

@app.route('/marco_teorico')
def theory():
    return render_template('theory.html')

@app.route('/map')
def map():
    return render_template('map.html')
if __name__ == "__main__":
    app.run(debug=True)