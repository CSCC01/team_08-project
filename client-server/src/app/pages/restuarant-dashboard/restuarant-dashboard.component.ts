import { Component, OnInit } from '@angular/core';
import orders from '../../../assets/data/orders.json';
import { ShowOnDirtyErrorStateMatcher } from '@angular/material/core';

@Component({
  selector: 'app-restuarant-dashboard',
  templateUrl: './restuarant-dashboard.component.html',
  styleUrls: ['./restuarant-dashboard.component.scss'],
})
export class RestuarantDashboardComponent implements OnInit {
  new_orders: any[];
  in_progress: any[];
  complete: any[];
  orders: any[];

  constructor() {
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

  ngOnInit(): void {}
}
