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
  getCartItems(cartId): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/item/get_by_cart/`;
    const params = {
      cart_id: cartId,
    };
    return this.http.get<any>(endpoint, { params: params });
  }

  /*
  @Input: 
  @Output: 
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
  @Input: 
  @Output: 
  */
  editAmount(itemId, count): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/item/remove/`;
    const obj = {
      item_id: itemId,
      count: count,
    };
    return this.http.post<any>(endpoint, obj);
  }

  /*
  @Input: 
  @Output: 
  */
  updateStatus(cartId, status): Observable<any> {
    const endpoint = `${OrdersService.ORDER_ENDPOINT}/cart/update_status/`;
    const obj = {
      _id: cartId,
      status: status,
    };
    return this.http.post<any>(endpoint, obj);
  }
}
