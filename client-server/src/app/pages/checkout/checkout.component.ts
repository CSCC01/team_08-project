import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginService } from 'src/app/service/login.service';
import cartItems from '../../../assets/data/cart.json';
import { OrdersService } from 'src/app/service/orders.service';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { StaticSymbol } from '@angular/compiler';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss'],
})
export class CheckoutComponent implements OnInit {
  userId: string = '';
  cartId: string = '';
  restaurantId: string = '';

  cartItems: any[] = [];
  foodIds = new Map();

  total: number = 0;

  constructor(
    private loginService: LoginService,
    private restaurantsService: RestaurantsService,
    private orderService: OrdersService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userId = sessionStorage.getItem('userId');

    this.loginService.getUser({ email: this.userId }).subscribe((data) => {
      if (
        data.address == '' ||
        data.address == null ||
        data.phone == '' ||
        data.address == null
      ) {
        alert('Please complete your details to place an order!');
        this.router.navigate(['/profile']);
      }
    });

    this.orderService.getCarts(this.userId, false).subscribe((status) => {
      if (status.carts) {
        this.restaurantId = status.carts[0].restaurant_id;
        this.cartId = status.carts[0]._id;
        this.total = status.carts[0].price;

        this.orderService.getCartItems(this.cartId).subscribe((data) => {
          console.log(data);
          for (var i = 0; i < data.items.length; i++) {
            this.foodIds.set(data.items[i].food_id, data.items[i].count);
          }

          this.restaurantsService
            .getRestaurantFood(this.restaurantId)
            .subscribe((dishes) => {
              console.log(dishes);
              for (var j = 0; j < dishes.Dishes.length; j++) {
                if (this.foodIds.has(dishes.Dishes[j]._id)) {
                  dishes.Dishes[j].quantity = this.foodIds.get(
                    dishes.Dishes[j]._id
                  );
                  this.cartItems.push(dishes.Dishes[j]);
                }
              }
            });
        });
      }
    });

    //this.cartId = sessionStorage.getItem('cartId');

    // TO BE REPLACED WHEN CONNECTS TO DB
    // this.total = 0.0;
    // for (let i = 0; i < this.cartItems.length; i++) {
    //   this.total = this.total + this.cartItems[i].total;
    // }
  }
}
