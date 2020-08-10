import { Component, OnInit } from '@angular/core';
import { OrdersService } from 'src/app/service/orders.service';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { generalUtils } from '../../utils/general';
import { orderUtils } from '../../utils/orders';
import { LoginService } from 'src/app/service/login.service';

@Component({
  selector: 'app-all-transactions',
  templateUrl: './all-transactions.component.html',
  styleUrls: ['./all-transactions.component.scss'],
})
export class AllTransactionsComponent implements OnInit {
  cartItems: any[] = [];
  restaurantsCollected: any[] = [];
  restaurantFood = new Map();
  cartHistory: any[] = [];

  userName: string = '';
  userAddress: string = '';
  userPhone: string = '';
  cartId: string = '';
  restaurantId: string = '';
  userId: string = '';

  constructor(
    private loginService: LoginService,
    private orderService: OrdersService,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {
    this.userId = sessionStorage.getItem('userId');
    this.loginService.getUser({ email: this.userId }).subscribe((data) => {
      this.userPhone = data.phone;
      this.userName = data.name;
      this.userAddress = data.address;
    });
    this.loadOrderHistory(this.userId);
    this.cartHistory.sort(orderUtils.OrderStatusComparator);
  }

  //   gets a cart's items and pushes them onto cart
  getCartItems(cart) {
    this.orderService.getCartItems(cart._id).subscribe((data) => {
      data.items.forEach((item) => {
        let food = this.restaurantFood.get(item.food_id);
        // push the cart item onto the history
        item.dish_name = food.name;
        cart.dishes.push(item);
      });
    });
  }

  loadOrderHistory(userId) {
    this.orderService.getCarts(userId, true).subscribe((response) => {
      if (response.carts) {
        // for each cart
        response.carts.forEach((cart) => {
          cart.dishes = [];

          // add the cart's restaurant id to the list of restaurants for which we have collected food data
          this.restaurantsCollected.push(cart.restaurant_id);
          // get the associated food items
          this.restaurantsService
            .getRestaurantFood(cart.restaurant_id)
            .subscribe((dishes) => {
              // for each dish, make it accessible by id from restaurantFood map
              dishes.Dishes.forEach((dish) => {
                this.restaurantFood.set(dish._id, dish);
              });
              // get the cart's items after the food has been loaded
              this.getCartItems(cart);
            });
          cart.name = this.userName;
          cart.address = this.userAddress;
          cart.phone = this.userPhone;
          cart.user_email = this.userId;
          cart.id = generalUtils.shortenID(cart._id);
          this.cartHistory.push(cart);
        });
      }
    });
  }
}
