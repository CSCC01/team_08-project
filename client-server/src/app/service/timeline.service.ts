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
  @Input: JSON object restaurant_id, user_id, and content
  @Output: None

  Creates a post on the for the restaurant on their timeline.
  */
  createPost(postInfo): Observable<any> {
    const endpoint = `${TimelineService.TL_ENDPOINT}/post/upload/`;
    return this.http.post<any>(endpoint, postInfo);
  }

  /*
  @Input: JSON object post_id, user_id, and content
  @Output: None

  Creates a comment on the post using post id and user id.
  */
  createComment(commentInfo): Observable<any> {
    const endpoint = `${TimelineService.TL_ENDPOINT}/comment/upload/`;
    return this.http.post<any>(endpoint, commentInfo);
  }
}
