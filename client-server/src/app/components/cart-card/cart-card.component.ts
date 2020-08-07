import { Component, OnInit, Input } from '@angular/core';
import { OrdersService } from 'src/app/service/orders.service';

@Component({
  selector: 'app-cart-card',
  templateUrl: './cart-card.component.html',
  styleUrls: ['./cart-card.component.scss'],
})
export class CartCardComponent implements OnInit {
  @Input() dish: any;
  value: number = 0;
  total: number = 0;

  constructor(private orderService: OrdersService) {}

  ngOnInit(): void {
    this.value = this.dish.quantity;
    this.total = this.dish.price * this.value;
  }

  changeQuantity() {
    this.total = this.dish.price * this.value;
  }
}
