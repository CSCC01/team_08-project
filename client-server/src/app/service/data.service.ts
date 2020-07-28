import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private userIdSource = new BehaviorSubject('');
  userId = this.userIdSource.asObservable();

  private restaurantIdSource = new BehaviorSubject('');
  restaurantId = this.restaurantIdSource.asObservable();

  private roleSource = new BehaviorSubject('BU');
  role = this.roleSource.asObservable();

  constructor() {}

  changeUserId(id: string) {
    this.userIdSource.next(id);
  }

  changeRestaurantId(id: string) {
    this.restaurantIdSource.next(id);
  }

  changeRole(role: string) {
    this.roleSource.next(role);
  }
}
