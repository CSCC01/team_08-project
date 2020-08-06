import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantsService } from '../../service/restaurants.service';
import { OrdersService } from '../../service/orders.service';
import { LoginService } from '../../service/login.service';

@Component({
  selector: 'app-all-orders',
  templateUrl: './all-orders.component.html',
  styleUrls: ['./all-orders.component.scss'],
})
export class AllOrdersComponent implements OnInit {
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
    private ordersService: OrdersService,
    private loginService: LoginService
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
    console.log(this.orders);
  }

  getOrders(): void {
    this.orders = [];
    this.ordersService
      .getOrdersbyRestaurant(this.restaurantId)
      .subscribe((data) => {
        let order;
        for (let i = 0; i < data.carts.length; i++) {
          order = data.carts[0];
          console.log(order);
          this.loginService
            .getUser({ email: order.user_email })
            .subscribe((data) => {
              order.name = data.name;
              order.phone = data.phone;
            });
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
          order._id = order._id.slice(-5, -1);
          this.orders.push(order);
        }
        console.log(this.orders);
      });
  }

  getRestaurantFood(): void {
    this.restaurantsService
      .getRestaurantFood(this.restaurantId)
      .subscribe((data) => {
        this.dishes = data.Dishes;
      });
  }
}
