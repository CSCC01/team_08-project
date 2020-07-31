import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from 'src/app/service/data.service';
import { LoginService } from 'src/app/service/login.service';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss'],
})
export class CheckoutComponent implements OnInit {
  userId: string = '';
  role: string = '';

  constructor(
    private data: DataService,
    private loginService: LoginService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.userId = this.route.snapshot.queryParams.userId;

    this.data.changeUserId(this.userId);
    this.data.changeRole(this.role);

    this.loginService.getUser({ email: this.userId }).subscribe((data) => {
      if (
        data.address == '' ||
        data.address == null ||
        data.phone == '' ||
        data.address == null
      ) {
        alert('Please complete your details to place an order!');
        this.router.navigate(['/profile'], {
          queryParams: {
            role: this.role,
            userId: this.userId,
          },
        });
      }
    });
  }
}
