import { Component, OnInit } from '@angular/core';
import orders from '../../../assets/data/orders.json';
import { ShowOnDirtyErrorStateMatcher } from '@angular/material/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from 'src/app/service/data.service';

@Component({
  selector: 'app-restuarant-dashboard',
  templateUrl: './restuarant-dashboard.component.html',
  styleUrls: ['./restuarant-dashboard.component.scss'],
})
export class RestuarantDashboardComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';

  new_orders: any[];
  in_progress: any[];
  complete: any[];
  orders: any[];

  constructor(
    private data: DataService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.orders = orders;
    this.new_orders = [];
    this.in_progress = [];
    this.complete = [];
    for (let i = 0; i < this.orders.length; i++) {
      if (this.orders[i].AccDec_Timestamp === '') {
        this.new_orders.push(this.orders[i]);
      } else if (
        this.orders[i].AccDec_Timestamp !== '' &&
        this.orders[i].Complete_Timestamp === ''
      ) {
        this.in_progress.push(this.orders[i]);
      } else {
        this.complete.push(this.orders[i]);
      }
    }
  }

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.userId = this.route.snapshot.queryParams.userId;
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    if (!this.restaurantId || this.role !== 'RO' || !this.userId) {
      this.router.navigate([''], {
        queryParams: {
          role: this.role,
          userId: this.userId,
          restaurantId: this.restaurantId,
        },
      });
      alert('No matching restaurant found for this profile!');
    }
    this.data.changeRestaurantId(this.restaurantId);
    this.data.changeUserId(this.userId);
    this.data.changeRole(this.role);
  }
}
