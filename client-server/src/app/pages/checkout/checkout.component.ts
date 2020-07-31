import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginService } from 'src/app/service/login.service';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss'],
})
export class CheckoutComponent implements OnInit {
  userId: string = '';

  constructor(
    private loginService: LoginService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userId = sessionStorage.getItem('userId');

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
