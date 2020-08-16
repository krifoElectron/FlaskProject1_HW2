from flask import Flask, render_template
from functools import reduce
from itertools import chain
from data import title, subtitle, description, departures, tours

app = Flask(__name__)

departure_list = [{'departure': departure[0], 'departure_display_name': departure[1]} for departure in
                  departures.items()]

tour_list = reduce(
    lambda prev, t: prev + [dict(chain.from_iterable(d.items() for d in ({'id': t[0]}, t[1])))], tours.items(),
    [])


@app.route('/')
def render_main():
    return render_template('index.html', title=title, subtitle=subtitle, description=description, tour_list=tour_list,
                           departure_list=departure_list, role='jjj', admin='asdf')


@app.route('/departures/<departure>/')
def render_departures(departure):
    departure_display_name = departures[departure][2:]
    filtered_tour_list = list(filter(lambda tour: tour['departure'] == departure, tour_list))

    number_of_tours = len(filtered_tour_list)
    price_list = reduce(lambda prev, tour: prev + [tour['price']], filtered_tour_list, [])
    min_price = min(price_list)
    max_price = max(price_list)

    night_list = reduce(lambda prev, tour: prev + [tour['nights']], filtered_tour_list, [])
    min_nights = min(night_list)
    max_nights = max(night_list)

    return render_template('departure.html', title=title, departure=departure, departure_list=departure_list,
                           departure_display_name=departure_display_name, filtered_tour_list=filtered_tour_list,
                           number_of_tours=number_of_tours, min_price=min_price, max_price=max_price,
                           min_nights=min_nights, max_nights=max_nights)


@app.route('/tours/<tour_id>')
def render_tour(tour_id):
    tour = tours[int(tour_id)]

    name = tour['title']
    number_of_starts = int(tour['stars'])
    to = tour['country']
    from_where = departures[tour['departure']]
    nights = tour['nights']
    picture = tour['picture']

    tour_description = tour['description']
    price = tour['price']

    return render_template('tour.html', title=title, departure_list=departure_list, name=name,
                           number_of_starts=number_of_starts, to=to, from_where=from_where, nights=nights,
                           picture=picture, tour_description=tour_description, price=price)


app.run(debug=True)
