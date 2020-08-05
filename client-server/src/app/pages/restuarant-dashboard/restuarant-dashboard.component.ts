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

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private restaurantsService: RestaurantsService,
    private ordersService: OrdersService
  ) {
    this.getOrders();
  }

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
  }

  getOrders(): void {
    this.ordersService
      .getOrdersbyRestaurant(this.restaurantId)
      .subscribe((data) => {
        for (let i = 0; i < data.length; i++) {
          if (data[i].complete_tstmp) {
            this.complete.push(data[i]);
          } else if (data[i].accept_tstmp) {
            this.in_progress.push(data[i]);
          } else {
            this.new_orders.push(data[i]);
          }
        }
      });
  }
}
