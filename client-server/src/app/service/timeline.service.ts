import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class TimelineService {
  private static readonly TL_ENDPOINT = `${environment.endpoint_url}/timeline`;

  constructor(private http: HttpClient) {}

  /*
  @Input: None
  @Output: List of all posts

  Retrieves all posts in the database.
  */
  getAllPosts(): Observable<any> {
    const endpoint = `${TimelineService.TL_ENDPOINT}/post/get_all/`;
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: List of all posts by a restaurant

  Retrieves all posts from restaurant in the database using restaurant id.
  */
  getRestaurantPosts(restaurantId): Observable<any> {
    const endpoint = `${TimelineService.TL_ENDPOINT}/post/get_by_restaurant/`;
    const params = {
      restaurant_id: restaurantId,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: Comment id
  @Output: Comment data

  Retrieves comment from database using comment id.
  */
  getComment(commentId): Observable<any> {
    const endpoint = `${TimelineService.TL_ENDPOINT}/comment/get/`;
    const params = {
      _id: commentId,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: JSON object restaurant_id, user_email, and content
  @Output: None

  Creates a post on the for the restaurant on their timeline.
  */
  createPost(postInfo): Observable<any> {
    const endpoint = `${TimelineService.TL_ENDPOINT}/post/upload/`;
    return this.http.post<any>(endpoint, postInfo);
  }

  /*
  @Input: JSON object post_id, user_email, and content
  @Output: None

  Creates a comment on the post using post id and user id.
  */
  createComment(commentInfo): void {
    const endpoint = `${TimelineService.TL_ENDPOINT}/comment/upload/`;
    this.http.post<any>(endpoint, commentInfo).subscribe((data) => {});
  }

  /*
  @Input: Post id of the post to be deleted
  @Output: None

  Deletes a post using post id.
  */
  deletePost(postId): void {
    const endpoint = `${TimelineService.TL_ENDPOINT}/post/delete/`;
    const postObj = {
      post_id: postId,
    };
    this.http.post<any>(endpoint, postObj).subscribe((data) => {});
  }

  /*
  @Input: Comment id of the comment to be deleted
  @Output: None

  Deletes a comment using comment id.
  */
  deleteComment(commentId): void {
    const endpoint = `${TimelineService.TL_ENDPOINT}/comment/delete/`;
    const commentObj = {
      _id: commentId,
    };
    this.http.post<any>(endpoint, commentObj).subscribe((data) => {});
  }
}
