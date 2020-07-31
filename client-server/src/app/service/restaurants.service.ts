import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class RestaurantsService {
  private static readonly RO_ENDPOINT = `${environment.endpoint_url}/restaurant`;
  private static readonly UPLOAD_ENDPOINT = `${environment.endpoint_url}/cloud_storage/upload/`;
  constructor(private http: HttpClient) {}

  /*
  @Input: None
  @Output: List of all restaurants

  Return list of all restaurants in the database
  */
  listRestaurants(): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/get_all/`;
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object

  Returns the details of the restaurant using its id.
  */
  getRestaurant(id): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/get/`;
    var params = {
      _id: id,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object with dishes

  Returns the details of the restaurant dishes using its id.
  */
  getRestaurantFood(id): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/dish/get_by_restaurant/`;
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
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/dish/get_all/`;
    return this.http.get(endpoint);
  }

  /*
  @Input: JSON object containing restaurant info
  @Output: The ID for that restaurant

  Creates an entry for the restauant in the database and returns an id
  */
  getRestaurantID(restuarantInfo): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/insert/`;
    return this.http.post<any>(endpoint, restuarantInfo);
  }

  /*
  @Input: JSON object containing dish info
  @Output: None

  Creates an entry for the dish for a particular restuarant using its id.
  */
  createDish(dishInfo): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/dish/insert/`;
    return this.http.post<any>(endpoint, dishInfo);
  }

  /*
  @Input: JSON object containing dish info
  @Output: None

  Creates an entry for the dish for a particular restuarant using its id.
  */
  editDish(dishInfo): Observable<any> {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/dish/edit/`;
    return this.http.post<any>(endpoint, dishInfo);
  }

  /*
  @Input: JSON object containing dish name and restaurant id
  @Output: None

  Delete dish using dish name and restaurant id.
  */
  deleteDish(dishInfo): void {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/dish/delete/`;
    this.http.post<any>(endpoint, dishInfo).subscribe((data) => {});
  }

  /*
  @Input: JSON object containing restaurant info (must have ID)
  @Output: None

  Edits information for a restuarant using its id.
  */
  editRestaurant(restInfo): void {
    const endpoint = `${RestaurantsService.RO_ENDPOINT}/edit/`;
    this.http.post<any>(endpoint, restInfo).subscribe((data) => {});
  }

  uploadRestaurantMedia(formData, id, location): Observable<any> {
    const endpoint = `${RestaurantsService.UPLOAD_ENDPOINT}`;

    if (location == 'cover') {
      formData.append('save_location', 'cover_photo_url');
    } else if (location == 'logo') {
      formData.append('save_location', 'logo_url');
    } else if (location == 'owner') {
      formData.append('save_location', 'owner_picture_url');
    }

    formData.append('app', 'restaurant_RestaurantMedia');
    formData.append('_id', id);

    return this.http.post<any>(endpoint, formData);
  }

  uploadFoodMedia(formData, id): Observable<any> {
    const endpoint = `${RestaurantsService.UPLOAD_ENDPOINT}`;

    formData.append('save_location', 'picture');
    formData.append('app', 'restaurant_FoodMedia');
    formData.append('_id', id);

    return this.http.post<any>(endpoint, formData);
  }
}
