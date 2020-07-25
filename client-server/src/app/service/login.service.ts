import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  private static readonly AUTH_ENDPOINT = `${environment.endpoint_url}/user`;

  constructor(private http: HttpClient) {}

  /*
  @Input: JSON user object from auth
  @Output: None
  Add logged in user to the database. Updates the time if user already exists.
  Assume user role for signup is "BU" (basic user) as this is the default
  */
  addNewUser(userData): void {
    const endpoint = `${LoginService.AUTH_ENDPOINT}/signup/`;
    this.http.post<any>(endpoint, userData).subscribe((data) => {});
  }

  /*
  @Input: JSON object from auth, restaurnt info from form
  @Output: None
  Assign the 'Restauraut Owner' role to the user using their email.
  */
  updateUser(userData): void {
    const endpoint = `${LoginService.AUTH_ENDPOINT}/reassign/`;
    const userObject = {
      email: userData._value.email,
      role: 'RO',
    };
    this.http.post<any>(endpoint, userObject).subscribe((data) => {});
  }

  /*
  @Input: JSON object from auth
  @Output: Return all fields of a user
  Get all fields of a user
  */
  getUser(userData): Observable<any> {
    const endpoint = `${LoginService.AUTH_ENDPOINT}/data/`;
    const userObject = {
      email: userData.email,
    };
    return this.http.get(endpoint, { params: userObject });
  }

  /*
  @Input: JSON object from auth
  @Output: Return True if user is in database, False otherwise
  Check if user exists in the database
  */
  checkUserExists(userData): Observable<any> {
    const endpoint = `${LoginService.AUTH_ENDPOINT}/exists/`;
    const userObject = {
      email: userData.email,
    };
    return this.http.get(endpoint, { params: userObject });
  }
}
