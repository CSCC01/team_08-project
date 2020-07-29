import { Component, OnInit } from '@angular/core';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantsService } from '../../service/restaurants.service';
import { DataService } from 'src/app/service/data.service';
import { LoginService } from 'src/app/service/login.service';

@Component({
  selector: 'app-all-restaurants',
  templateUrl: './all-restaurants.component.html',
  styleUrls: ['./all-restaurants.component.scss'],
})
export class AllRestaurantsComponent implements OnInit {
  userId: string = '';
  role: string = '';

  restaurants: any[];
  dishes: any[];
  faSearch = faSearch;

  constructor(
    private restaurantsService: RestaurantsService,
    private loginService: LoginService,
    private data: DataService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.userId = this.route.snapshot.queryParams.userId;

    this.data.changeUserId(this.userId);
    this.data.changeRole(this.role);

    // Get user long and lat
    // this.loginService.getUser({ email: this.userId }).subscribe((data) => {
    //   console.log(data);
    // });

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
