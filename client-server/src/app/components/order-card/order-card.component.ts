import { Component, OnInit, Input } from '@angular/core';
import { OrdersService } from '../../service/orders.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-order-card',
  templateUrl: './order-card.component.html',
  styleUrls: ['./order-card.component.scss'],
})
export class OrderCardComponent implements OnInit {
  @Input() order: any;
  modalRef: any;

  constructor(
    private ordersService: OrdersService,
    private modalService: NgbModal
  ) {}

  ngOnInit(): void {}

  acceptOrder(): void {
    console.log('hi');
    this.updateStatusofCart('acc');
  }

  completeOrder(): void {
    this.updateStatusofCart('cmt');
  }

  cancelOrder(): void {
    this.ordersService.cancelCart(this.order._id).subscribe();
    setTimeout(function () {
      window.location.reload();
    }, 100);
  }

  updateStatusofCart(status): void {
    this.ordersService.updateStatus(this.order._id, status).subscribe();
    setTimeout(function () {
      window.location.reload();
    }, 100);
  }

  openModal(content) {
    this.modalRef = this.modalService.open(content);
  }
}
