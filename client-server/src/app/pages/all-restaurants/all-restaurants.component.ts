import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { RestaurantsService } from '../../service/restaurants.service';
import { geolocation } from '../../utils/geolocation';

@Component({
  selector: 'app-all-restaurants',
  templateUrl: './all-restaurants.component.html',
  styleUrls: ['./all-restaurants.component.scss'],
})
export class AllRestaurantsComponent implements OnInit {
  userId: string = '';
  role: string = '';

  allRestaurants: any[];
  allDishes: any[];

  restaurants: any[];
  dishes: any[];
  inputRestaurant: string = '';
  inputDishes: string = '';

  LONGITUDE_PROPERTY_NAME: string = 'lng';
  LATITUDE_PROPERTY_NAME: string = 'lat';

  faSearch = faSearch;

  constructor(private restaurantsService: RestaurantsService) {}

  ngOnInit(): void {
    this.loadRestaurants();
    this.loadDishes();
  }

  loadRestaurants() {
    this.restaurantsService.listRestaurants().subscribe((data) => {
      this.restaurants = data.Restaurants;
      this.allRestaurants = data.Restaurants;
      navigator.geolocation.getCurrentPosition((positon) => {
        for (var i = 0; i < this.restaurants.length; i++) {
          var index = this.restaurants[i];

          if (index.GEO_location != 'blank' && index.GEO_location != '') {
            var GEOJson = JSON.parse(index.GEO_location.replace(/\'/g, '"'));
            if (
              GEOJson[this.LONGITUDE_PROPERTY_NAME] != undefined &&
              GEOJson[this.LATITUDE_PROPERTY_NAME] != undefined
            ) {
              this.restaurants[
                i
              ].distanceFromUser = geolocation.haversineDistance(
                GEOJson[this.LATITUDE_PROPERTY_NAME],
                GEOJson[this.LONGITUDE_PROPERTY_NAME],
                positon.coords.latitude,
                positon.coords.longitude
              );
            }
          }
        }
        this.restaurants = this.sortClosestCurrentLoc(this.restaurants);
        this.allRestaurants = this.restaurants;
      });
    });
  }

  loadDishes() {
    this.restaurantsService.getDishes().subscribe((data) => {
      this.dishes = data.Dishes;
      this.allDishes = data.Dishes;
    });
  }

  filterRating(list) {
    this.restaurants = [];
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      this.loadRestaurants();
    } else {
      for (var i = 0; i < this.allRestaurants.length; i++) {
        var query = this.allRestaurants[i];
        if (list[0] == true && query.rating <= 1) {
          this.restaurants.push(query);
        }

        if (list[1] == true && query.rating > 1 && query.rating <= 2) {
          this.restaurants.push(query);
        }

        if (list[2] == true && query.rating > 2 && query.rating <= 3) {
          this.restaurants.push(query);
        }

        if (list[3] == true && query.rating > 3 && query.rating <= 4) {
          this.restaurants.push(query);
        }

        if (list[4] == true && query.rating > 4) {
          this.restaurants.push(query);
        }
      }
    }
  }

  sortClosestCurrentLoc(restaurants: Array<any>) {
    return restaurants.sort((rest1, rest2) => {
      let result = 0;
      let valid1 = rest1.hasOwnProperty('distanceFromUser');
      let valid2 = rest2.hasOwnProperty('distanceFromUser');
      if (!valid1 && valid2) return 0;
      // if only one is invalid, return a really high weight in direction of the valid one
      if (!valid1) {
        return 1000;
      }
      if (!valid2) {
        return -1000;
      }
      return rest1.distanceFromUser - rest2.distanceFromUser;
    });
  }

  filterPricepoint(list) {
    this.restaurants = [];
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      this.loadRestaurants();
    } else {
      for (var i = 0; i < this.allRestaurants.length; i++) {
        var query = this.allRestaurants[i];
        if (list[0] == true && query.pricepoint == 'Low') {
          this.restaurants.push(query);
        }

        if (list[1] == true && query.pricepoint == 'Medium') {
          this.restaurants.push(query);
        }

        if (list[2] == true && query.pricepoint == 'High') {
          this.restaurants.push(query);
        }
      }
    }
  }

  filterPrice(list) {
    this.dishes = [];
    const isFalse = (currentValue) => !currentValue;

    if (list.every(isFalse)) {
      this.loadDishes();
    } else {
      for (var i = 0; i < this.allDishes.length; i++) {
        var query = this.allDishes[i];
        if (list[0] == true && query.price <= 20) {
          this.dishes.push(query);
        }

        if (list[1] == true && query.price > 20 && query.price <= 40) {
          this.dishes.push(query);
        }

        if (list[2] == true && query.price > 40 && query.price <= 60) {
          this.dishes.push(query);
        }

        if (list[3] == true && query.price > 60) {
          this.dishes.push(query);
        }
      }
    }
  }

  searchRestaurants() {
    if (this.inputRestaurant == '') {
      this.loadRestaurants();
    } else {
      this.restaurants = [];
      for (var i = 0; i < this.allRestaurants.length; i++) {
        var query = this.allRestaurants[i];
        if (
          query.name
            .toLowerCase()
            .includes(this.inputRestaurant.toLowerCase()) ||
          query.cuisine
            .toLowerCase()
            .includes(this.inputRestaurant.toLowerCase()) ||
          query.pricepoint
            .toLowerCase()
            .includes(this.inputRestaurant.toLowerCase()) ||
          query.owner_name
            .toLowerCase()
            .includes(this.inputRestaurant.toLowerCase())
        ) {
          this.restaurants.push(query);
        }
      }
    }
  }

  searchDishes() {
    if (this.inputDishes == '') {
      this.loadDishes();
    } else {
      this.dishes = [];
      for (var i = 0; i < this.allDishes.length; i++) {
        var query = this.allDishes[i];
        if (
          query.name.toLowerCase().includes(this.inputDishes.toLowerCase()) ||
          query.price.toLowerCase().includes(this.inputDishes.toLowerCase())
        ) {
          this.dishes.push(query);
        }
      }
    }
  }
}
