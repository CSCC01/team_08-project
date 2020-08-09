import { Component, OnInit } from '@angular/core';
import {
  faCreditCard,
  faUser,
  faCalendarAlt,
  faKey,
  faHome,
  faBuilding,
  faCity,
} from '@fortawesome/free-solid-svg-icons';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { OrdersService } from 'src/app/service/orders.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.scss'],
})
export class PaymentComponent implements OnInit {
  faCreditCard = faCreditCard;
  faUser = faUser;
  faCalendarAlt = faCalendarAlt;
  faKey = faKey;
  faHome = faHome;
  faBuilding = faBuilding;
  faCity = faCity;

  cartId: string = '';
  modalRef: any;

  timeLeft: number = 30;
  interval: any;

  constructor(
    private orderService: OrdersService,
    private route: ActivatedRoute,
    private router: Router,
    private modalService: NgbModal
  ) {}

  ngOnInit(): void {
    AOS.init({
      delay: 300,
      duration: 1500,
      once: false,
      anchorPlacement: 'top-bottom',
    });

    this.cartId = sessionStorage.getItem('cartId');
  }

  openModal(content) {
    this.modalRef = this.modalService.open(content, { size: 's' });
    this.interval = setInterval(() => {
      if (this.timeLeft > 0) {
        this.timeLeft--;
      } else {
        this.timeLeft = 30;
      }
    }, 1000);
    setTimeout(() => this.payCart(), 30000);
  }

  payCart() {
    this.orderService.updateStatus(this.cartId, 'snd').subscribe((data) => {
      alert('Thank you for your order!');
      this.modalRef.close();
      this.router.navigate(['/']);
    });
  }

  backToCart() {
    this.modalRef.close();
    this.router.navigate(['/checkout']);
  }
}
