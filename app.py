from flask import Flask, render_template
from data import title, subtitle, description, departures, tours

app = Flask(__name__)

departure_list = [{'departure': departure[0], 'departure_display_name': departure[1]} for departure in
                  departures.items()]

tour_list = [{'id': tour_id, **tour} for tour_id, tour in tours.items()]


@app.route('/')
def render_main():
    return render_template('index.html', title=title, subtitle=subtitle, description=description,
                           tour_list=tour_list[:6], departure_list=departure_list)


@app.route('/departures/<departure>/')
def render_departures(departure):
    departure_display_name = departures[departure][2:]
    filtered_tour_list = [tour for tour in tour_list if tour['departure'] == departure]

    number_of_tours = len(filtered_tour_list)
    price_list = [tour['price'] for tour in filtered_tour_list]
    min_price = min(price_list)
    max_price = max(price_list)

    night_list = [tour['nights'] for tour in filtered_tour_list]
    min_nights = min(night_list)
    max_nights = max(night_list)

    return render_template('departure.html', title=title, departure=departure, departure_list=departure_list,
                           departure_display_name=departure_display_name, filtered_tour_list=filtered_tour_list,
                           number_of_tours=number_of_tours, min_price=min_price, max_price=max_price,
                           min_nights=min_nights, max_nights=max_nights)


@app.route('/tours/<int:tour_id>')
def render_tour(tour_id):
    tour = tours[tour_id]

    name = tour['title']
    number_of_starts = int(tour['stars'])
    to = tour['country']
    from_where = f'и{departures[tour["departure"]][1:]}'
    nights = tour['nights']
    picture = tour['picture']

    tour_description = tour['description']
    price = tour['price']

    return render_template('tour.html', title=title, departure_list=departure_list, name=name,
                           number_of_starts=number_of_starts, to=to, from_where=from_where, nights=nights,
                           picture=picture, tour_description=tour_description, price=price)


if __name__ == '__main__':
    app.run()
