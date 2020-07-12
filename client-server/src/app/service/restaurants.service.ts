import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class RestaurantsService {
  private static readonly RO_ENDPOINT = `${environment.endpoint_url}`;

  constructor(private http: HttpClient) {}

  /*
  @Input: None
  @Output: List of all restaurants

  Return list of all restaurants in the database
  */
  listRestaurants(): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/RO/getAll/`;
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object

  Returns the details of the restaurant using its id.
  */
  getRestaurant(id): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/RO/get/`;
    var params = {
      _id: id,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object

  Returns the details of the restaurant using its id.
  */
  getRestaurantFood(id): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/tag/get_food_by_restaurant/`;
    var params = {
      restaurant_id: id,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: None
  @Output: All Dishes

  Returns All Dishes.
  */
  getDishes(): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/tag/get_all/`;
    return this.http.get(endpoint);
  }
}