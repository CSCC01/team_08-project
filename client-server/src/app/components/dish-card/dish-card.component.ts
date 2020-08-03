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
  value: number = 0;
  modalRef: any;

  @Input() dish: any;

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
    var cardId = sessionStorage.getItem('cartId');

    if (cardId == '') {
      this.orderService
        .insertCart(this.dish.restaurant_id, this.userId)
        .subscribe((data) => {
          sessionStorage.setItem('cartId', data._id);
        });
    }

    if (this.value != 0) {
      this.orderService.insertItem(cardId, this.dish._id, this.value);
    } else {
      alert('Please have a non-zero amount for the dish!');
    }
    this.modalRef.close();
  }
}
