import { Component, OnInit } from '@angular/core';
import orders from '../../../assets/data/orders.json';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-restuarant-dashboard',
  templateUrl: './restuarant-dashboard.component.html',
  styleUrls: ['./restuarant-dashboard.component.scss'],
})
export class RestuarantDashboardComponent implements OnInit {
  restaurantId: string = '';
  restaurantName: string = '';
  userId: string = '';
  role: string = '';

  new_orders: any[];
  in_progress: any[];
  complete: any[];
  orders: any[];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private restaurantsService: RestaurantsService
  ) {
    // this.orders = orders;
    // this.new_orders = [];
    // this.in_progress = [];
    // this.complete = [];
    // for (let i = 0; i < this.orders.length; i++) {
    //   if (this.orders[i].AccDec_Timestamp === '') {
    //     this.new_orders.push(this.orders[i]);
    //   } else if (
    //     this.orders[i].AccDec_Timestamp !== '' &&
    //     this.orders[i].Complete_Timestamp === ''
    //   ) {
    //     this.in_progress.push(this.orders[i]);
    //   } else {
    //     this.complete.push(this.orders[i]);
    //   }
    // }
  }

  ngOnInit(): void {
    this.restaurantId = sessionStorage.getItem('restaurantId');
    if (!this.restaurantId) {
      this.router.navigate(['']);
      alert('No matching restaurant found for this profile!');
    }
    this.restaurantsService
      .getRestaurant(this.restaurantId)
      .subscribe((data) => {
        this.restaurantName = data.name;
      });
  }

  getOrders(): void {}
}
