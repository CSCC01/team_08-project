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
  @Input: 
  @Output: 
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
  @Input: 
  @Output: 
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
  @Input: 
  @Output: 
  */
  removeItem(itemId): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/item/remove/`;
    const obj = {
      item_id: itemId,
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
  @Input: A cart ID and a boolean for status
  @Output: None

  Updates the status of the cart
  */
  updateStatus(cartId, status): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/cart/update_status/`;
    const obj = {
      _id: cartId,
      status: status,
    };
    console.log(obj);
    return this.http.post<any>(endpoint, obj);
  }
}
