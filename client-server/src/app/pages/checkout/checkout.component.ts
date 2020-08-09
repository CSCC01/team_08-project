import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { LoginService } from 'src/app/service/login.service';
import { OrdersService } from 'src/app/service/orders.service';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { orderUtils } from '../../utils/orders';
import { generalUtils } from '../../utils/general';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss'],
})
export class CheckoutComponent implements OnInit {
  userId: string = '';
  //   needed for order history card
  userName: string = '';
  userAddress: string = '';
  userPhone: string = '';
  cartId: string = '';
  restaurantId: string = '';

  cartItems: any[] = [];
  foodIds = new Map();

  cartHistory: any[] = [];
  restaurantsCollected: any[] = [];
  restaurantFood = new Map();

  total: number = 0;

  faTrash = faTrash;

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
        data.phone == null
      ) {
        alert('Please complete your details to place an order!');
        this.router.navigate(['/profile']);
      } else {
        this.userPhone = data.phone;
        this.userName = data.name;
        this.userAddress = data.address;
      }
    });

    this.loadCart();
    this.loadOrderHistory(this.userId);
    this.cartHistory.sort(orderUtils.OrderStatusComparator);
  }

  loadCart() {
    this.cartId = sessionStorage.getItem('cartId');
    this.cartItems = [];
    this.orderService.getCarts(this.userId, false).subscribe((status) => {
      if (status.carts) {
        this.restaurantId = status.carts[0].restaurant_id;
        this.cartId = status.carts[0]._id;
        this.total = status.carts[0].price;

        this.orderService.getCartItems(this.cartId).subscribe((data) => {
          for (var i = 0; i < data.items.length; i++) {
            this.foodIds.set(data.items[i].food_id, [
              data.items[i].count,
              data.items[i]._id,
            ]);
          }

          this.restaurantsService
            .getRestaurantFood(this.restaurantId)
            .subscribe((dishes) => {
              for (var j = 0; j < dishes.Dishes.length; j++) {
                if (this.foodIds.has(dishes.Dishes[j]._id)) {
                  dishes.Dishes[j].quantity = this.foodIds.get(
                    dishes.Dishes[j]._id
                  )[0];
                  dishes.Dishes[j].itemId = this.foodIds.get(
                    dishes.Dishes[j]._id
                  )[1];
                  this.cartItems.push(dishes.Dishes[j]);
                }
              }
            });
        });
      }
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

  deleteOrder(dish) {
    var itemId = this.foodIds.get(dish._id)[1];
    this.orderService.removeItem(itemId).subscribe(
      (data) => {
        this.loadCart();
      },
      (error) => {
        window.location.reload();
      }
    );
  }

  clearCart() {
    this.orderService.clearCart(this.cartId).subscribe(
      (data) => {
        window.location.reload();
      },
      (error) => {
        window.location.reload();
      }
    );
  }
}
