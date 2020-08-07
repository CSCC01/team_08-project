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

  constructor(
    private orderService: OrdersService,
    private route: ActivatedRoute,
    private router: Router
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

  payCart() {
    this.orderService.updateStatus(this.cartId, 'snd').subscribe((data) => {
      alert('Thank you for your order!');
      this.router.navigate(['/']);
    });
  }
}
