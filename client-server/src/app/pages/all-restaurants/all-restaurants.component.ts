import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-all-restaurants',
  templateUrl: './all-restaurants.component.html',
  styleUrls: ['./all-restaurants.component.scss'],
})
export class AllRestaurantsComponent implements OnInit {
  restaurants: any[];
  dishes: any[];
  faSearch = faSearch;

  constructor(private restaurantsService: RestaurantsService) {}

  ngOnInit(): void {
    // Get list of all restaurants
    this.restaurantsService.listRestaurants().subscribe((data) => {
      this.restaurants = data.Restaurants;
    });
    this.restaurantsService.getDishes().subscribe((data) => {
      this.dishes = data.Dishes;
    });
  }

  displayList(list) {}
}
