import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantsService } from '../../service/restaurants.service';
import { OrdersService } from '../../service/orders.service';

@Component({
  selector: 'app-restuarant-dashboard',
  templateUrl: './restuarant-dashboard.component.html',
  styleUrls: ['./restuarant-dashboard.component.scss'],
})
export class RestuarantDashboardComponent implements OnInit {
  restaurantId: string = '';
  restaurantName: string = '';
  userId: string = '';
  role: string = '';

  new_orders: any[];
  in_progress: any[];
  complete: any[];
  orders: any[];
  dishes: any[];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private restaurantsService: RestaurantsService,
    private ordersService: OrdersService
  ) {}

  ngOnInit(): void {
    this.restaurantId = sessionStorage.getItem('restaurantId');
    if (!this.restaurantId) {
      this.router.navigate(['']);
      alert('No matching restaurant found for this profile!');
    }
    this.restaurantsService
      .getRestaurant(this.restaurantId)
      .subscribe((data) => {
        this.restaurantName = data.name;
      });
    this.getRestaurantFood();
    this.getOrders();
  }

  getOrders(): void {
    this.orders = [];
    this.new_orders = [];
    this.in_progress = [];
    this.complete = [];
  }

  getRestaurantFood(): void {
    this.restaurantsService
      .getRestaurantFood(this.restaurantId)
      .subscribe((data) => {
        this.dishes = data.Dishes;
      });
  }

  viewAllOrders(): void {
    this.router.navigate(['/all-orders']);
  }
}
