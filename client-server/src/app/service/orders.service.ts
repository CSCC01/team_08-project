import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class OrdersService {
  private static readonly ORDER_ENDPOINT = `${environment.endpoint_url}/order`;

  constructor(private http: HttpClient) {}

  /*
  @Input: Object with restaurant id (where you are ordering from) and user email
  @Output: None

  Create a cart for a user.
  */
  insertCart(restaurantId, email): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/cart/insert/`;
    const obj = {
      restaurant_id: restaurantId,
      user_email: email,
    };
    return this.http.post<any>(endpoint, obj);
  }

  /*
  @Input: Cart id
  @Output: List of items in the cart

  Get a list of items in a particular cart.
  */
  getCartItems(cartId): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/item/get_by_cart/`;
    const params = {
      cart_id: cartId,
    };
    return this.http.get<any>(endpoint, { params: params });
  }

  /*
  @Input: Object with user email and sent status (either true or false)
  @Output: List of carts that are send (true), or list of carts not yet sent (false)

  Get a list of carts for a user based on sent status.
  */
  getCarts(userId, sent): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/cart/user_carts/`;
    const params = {
      user_email: userId,
      is_sent: sent,
    };
    return this.http.get<any>(endpoint, { params: params });
  }

  /*
  @Input: Cart id to clear
  @Output: None

  Clear all items from a cart and delete the cart.
  */
  clearCart(cartId): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/cart/cancel/`;
    const obj = {
      _id: cartId,
    };
    return this.http.post<any>(endpoint, obj);
  }

  /*
  @Input: Object with cart id, food id, and food amount
  @Output: None

  Add a certain amount of items to the cart.
  */
  insertItem(cartId, foodId, count): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/item/insert/`;
    const obj = {
      cart_id: cartId,
      food_id: foodId,
      count: count,
    };
    return this.http.post<any>(endpoint, obj);
  }

  /*
  @Input: Item id of item to remove
  @Output: None

  Remove an item from cart.
  */
  removeItem(itemId): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/item/remove/`;
    const obj = {
      item_id: itemId,
    };
    return this.http.post<any>(endpoint, obj);
  }

  /*
  @Input: Object with item id and new amount
  @Output: None

  Edit the amount of an item in the cart.
  */
  editAmount(itemId, count): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/item/edit_amount/`;
    const obj = {
      item_id: itemId,
      count: count,
    };
    return this.http.post<any>(endpoint, obj);
  }
  
  /*
  @Input: A restaurant ID
  @Output: All orders for a particular restaruant

  Get all orders by restaurant
  */
  getOrdersbyRestaurant(restaurantId): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/cart/restaurant_carts/`;
    var params = {
      restaurant_id: restaurantId,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: A cart ID
  @Output: All items for a cart

  Get all items in a cart
  */
  getItembyCart(cartId): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/item/get_by_cart/`;
    var params = {
      cart_id: cartId,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: Object with cart id to update and status (snd, cmt, acc)
  @Output: None

  Update a cart status to send it through the ordering process.
  */
  updateStatus(cartId, status): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/cart/update_status/`;
    const obj = {
      _id: cartId,
      status: status,
    };
    return this.http.post<any>(endpoint, obj);
  }

  /*
  @Input: A cart ID and a boolean for status
  @Output: None

  Updates the status of the cart
  */
  cancelCart(cartId): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/cart/cancel/`;
    const obj = {
      _id: cartId,
    };
    return this.http.post<any>(endpoint, obj);
  }
}
