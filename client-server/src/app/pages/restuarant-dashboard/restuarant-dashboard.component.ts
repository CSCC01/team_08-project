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
    this.ordersService
      .getOrdersbyRestaurant(this.restaurantId)
      .subscribe((data) => {
        let order;
        for (let i = 0; i < data.carts.length; i++) {
          order = data.carts[0];
          order.dishes = [];
          this.ordersService.getItembyCart(order._id).subscribe((data) => {
            for (let j = 0; j < data.items.length; j++) {
              order.dishes[i] = {
                count: data.items[j].count,
                dish: data.items[j].food_id,
              };

              this.dishes.forEach((element) => {
                if (element._id == data.items[j].food_id) {
                  order.dishes[i].dish_name = element.name;
                }
              });
            }
          });
          this.orders.push(order);
        }
        console.log(this.orders);

        // for (let i = 0; i < data.length; i++) {
        //   if (data[i].complete_tstmp) {
        //     this.complete.push(data[i]);
        //   } else if (data[i].accept_tstmp) {
        //     this.in_progress.push(data[i]);
        //   } else {
        //     this.new_orders.push(data[i]);
        //   }
        // }
      });
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
