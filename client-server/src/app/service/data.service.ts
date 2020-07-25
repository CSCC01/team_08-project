import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private restaurantIdSource = new BehaviorSubject('default id');
  restaurantId = this.restaurantIdSource.asObservable();

  private roleSource = new BehaviorSubject('BU');
  role = this.roleSource.asObservable();

  constructor() {}

  changeRestaurantId(id: string) {
    this.restaurantIdSource.next(id);
  }

  changeRole(role: string) {
    this.roleSource.next(role);
  }
}
