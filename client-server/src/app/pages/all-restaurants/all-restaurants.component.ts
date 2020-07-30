import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantsService } from '../../service/restaurants.service';
import { DataService } from 'src/app/service/data.service';

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

  faSearch = faSearch;

  constructor(
    private restaurantsService: RestaurantsService,
    private data: DataService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.userId = this.route.snapshot.queryParams.userId;

    this.data.changeUserId(this.userId);
    this.data.changeRole(this.role);

    this.loadRestaurants();
    this.loadDishes();
  }

  loadRestaurants() {
    this.restaurantsService.listRestaurants().subscribe((data) => {
      this.restaurants = data.Restaurants;
      this.allRestaurants = data.Restaurants;
    });
  }

  loadDishes() {
    this.restaurantsService.getDishes().subscribe((data) => {
      this.dishes = data.Dishes;
      this.allDishes = data.Dishes;
    });
  }

  filterList(list, filter) {}

  searchRestaurants() {
    if (this.inputRestaurant == '') {
      this.restaurants = this.allRestaurants;
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
      this.dishes = this.allDishes;
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
