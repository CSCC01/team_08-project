import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import { LoginService } from 'src/app/service/login.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  userId: string = '';
  userInfo: any;
  constructor(public auth: AuthService, private loginService: LoginService) {}

  ngOnInit() {
    this.userId = sessionStorage.getItem('userId');
    this.loginService.getUser({ email: this.userId }).subscribe((data) => {
      this.userInfo = data;
    });
  }
}
