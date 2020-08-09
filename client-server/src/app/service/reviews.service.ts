import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ReviewsService {
  private static readonly REVIEW_ENDPOINT = `${environment.endpoint_url}/review`;

  constructor(private http: HttpClient) {}

  /*
  @Input: Review object
  @Output: None
  Add review to database for a restaurant
  */
  insertReview(review: any): Observable<any> {
    const endpoint = `${ReviewsService.REVIEW_ENDPOINT}/insert/`;
    return this.http.post<any>(endpoint, review);
  }

  /*
  @Input: Review object
  @Output: None
  Add review to database for a restaurant
  */
  getReviewbyRestaurant(restaurantId): Observable<any> {
    const endpoint = `${ReviewsService.REVIEW_ENDPOINT}/get_by_restaurant/`;
    var params = {
      restaurant_id: restaurantId,
    };
    return this.http.get(endpoint, { params: params });
  }
}
