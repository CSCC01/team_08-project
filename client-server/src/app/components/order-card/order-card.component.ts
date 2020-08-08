import { Component, OnInit, Input } from '@angular/core';
import { OrdersService } from '../../service/orders.service';

@Component({
  selector: 'app-order-card',
  templateUrl: './order-card.component.html',
  styleUrls: ['./order-card.component.scss'],
})
export class OrderCardComponent implements OnInit {
  @Input() order: any;

  constructor(private ordersService: OrdersService) {}

  ngOnInit(): void {}

  acceptOrder(): void {
    console.log('hi');
    this.updateStatusofCart('acc');
  }

  completeOrder(): void {
    this.updateStatusofCart('cmt');
  }

  updateStatusofCart(status): void {
    this.ordersService.updateStatus(this.order._id, status).subscribe();
    setTimeout(function () {
      window.location.reload();
    }, 100);
  }
}
