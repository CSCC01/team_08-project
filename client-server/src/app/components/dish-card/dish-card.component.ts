import { Component, OnInit, Input, HostListener } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { OrdersService } from 'src/app/service/orders.service';

@Component({
  selector: 'app-dish-card',
  exportAs: 'app-dish-card',
  templateUrl: './dish-card.component.html',
  styleUrls: ['./dish-card.component.scss'],
})
export class DishCardComponent implements OnInit {
  role: string = '';
  userId: string = '';
  cartId: string = '';
  value: number = 0;
  modalRef: any;

  @Input() dish: any;
  @Input() restaurantId: string;

  constructor(
    private orderService: OrdersService,
    private modalService: NgbModal
  ) {}

  @HostListener('window:resize', ['$event'])
  onResize() {
    var el1 = document.getElementById('col-img');
    var el2 = document.getElementById('col-body');
    var el3 = document.getElementById('row-modal');

    if (window.innerWidth < 1300) {
      el1.classList.remove('col-md-4');
      el2.classList.remove('col-md-8');
      el3.classList.remove('row');
    } else {
      el1.classList.add('col-md-4');
      el2.classList.add('col-md-8');
      el3.classList.add('row');
    }
  }

  ngOnInit(): void {
    this.role = sessionStorage.getItem('role');
    this.userId = sessionStorage.getItem('userId');
  }

  openDish(content) {
    this.modalRef = this.modalService.open(content, { size: 'xl' });
  }

  addOrder() {
    if (this.restaurantId == undefined) {
      this.restaurantId = this.dish.restaurant_id;
    }

    this.orderService.getCarts(this.userId, false).subscribe((status) => {
      if (status.carts) {
        this.cartId = status.carts[0]._id;
        sessionStorage.setItem('cartId', this.cartId);

        if (this.value != 0) {
          this.orderService
            .insertItem(this.cartId, this.dish._id, this.value)
            .subscribe((data) => {});
        } else {
          alert('Please have a non-zero amount for the dish!');
        }
      } else {
        this.orderService
          .insertCart(this.restaurantId, this.userId)
          .subscribe((data) => {
            this.cartId = data._id;
            sessionStorage.setItem('cartId', data._id);
            sessionStorage.setItem('restOrder', this.restaurantId);

            if (this.value != 0) {
              this.orderService
                .insertItem(this.cartId, this.dish._id, this.value)
                .subscribe((data) => {});
            } else {
              alert('Please have a non-zero amount for the dish!');
            }
          });
      }
    });

    this.modalRef.close();
  }
}
