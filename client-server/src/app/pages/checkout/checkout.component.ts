import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginService } from 'src/app/service/login.service';
import cartItems from '../../../assets/data/cart.json';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss'],
})
export class CheckoutComponent implements OnInit {
  userId: string = '';
  cartItems: any[];
  total: number;

  constructor(
    private loginService: LoginService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.cartItems = cartItems;
  }

  ngOnInit(): void {
    this.userId = sessionStorage.getItem('userId');

    // TO BE REPLACED WHEN CONNECTS TO DB
    this.total = 0.0;
    for (let i = 0; i < this.cartItems.length; i++) {
      this.total = this.total + this.cartItems[i].total;
    }

    this.loginService.getUser({ email: this.userId }).subscribe((data) => {
      if (
        data.address == '' ||
        data.address == null ||
        data.phone == '' ||
        data.address == null
      ) {
        alert('Please complete your details to place an order!');
        this.router.navigate(['/profile']);
      }
    });
  }
}
