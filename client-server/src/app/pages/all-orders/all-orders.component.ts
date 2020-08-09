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
  }

  getOrders(): void {
    this.orders = [];
    this.ordersService
      .getOrdersbyRestaurant(this.restaurantId)
      .subscribe((data) => {
        let cart;
        for (let i = 0; i < data.carts.length; i++) {
          cart = data.carts[i];
          cart.dishes = [];
          this.orders.push(cart);
        }

        this.getOrderNames();
        this.getOrderCartItems();
        this.shortenOrderID();
      });
  }

  getOrderNames(): void {
    for (let i = 0; i < this.orders.length; i++) {
      this.loginService
        .getUser({ email: this.orders[i].user_email })
        .subscribe((data) => {
          this.orders[i].name = data.name;
          this.orders[i].phone = data.phone;
        });
    }
  }

  getOrderCartItems(): void {
    for (let i = 0; i < this.orders.length; i++) {
      this.ordersService.getItembyCart(this.orders[i]._id).subscribe((data) => {
        for (let k = 0; k < data.items.length; k++) {
          let info = {
            count: data.items[k].count,
            dish: data.items[k].food_id,
            dish_name: '',
          };
          this.dishes.forEach((element) => {
            if (element._id == info.dish) {
              info.dish_name = element.name;
            }
          });
          this.orders[i].dishes.push(info);
        }
      });
    }
  }

  getRestaurantFood(): void {
    this.restaurantsService
      .getRestaurantFood(this.restaurantId)
      .subscribe((data) => {
        this.dishes = data.Dishes;
      });
  }

  shortenOrderID(): void {
    for (let i = 0; i < this.orders.length; i++) {
      this.orders[i].id = this.orders[i]._id.slice(-6);
    }
  }

  back(): void {
    this.router.navigate(['/dashboard']);
  }
}
