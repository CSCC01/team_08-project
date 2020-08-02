import { Component, OnInit, HostListener, AfterViewInit } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import { faUserCircle } from '@fortawesome/free-solid-svg-icons';
import { LoginService } from '../../service/login.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit, AfterViewInit {
  title: string = 'Scarborough Dining';

  restaurantId: string = '';
  role: string = '';
  userId: string = '';

  faUserCircle = faUserCircle;
  userRole: any;

  constructor(
    public auth: AuthService,
    private loginService: LoginService,
    private router: Router
  ) {}

  @HostListener('window:resize', ['$event'])
  onResize() {
    if (window.innerWidth < 650) {
      this.title = 'SDining';
    } else {
      this.title = 'Scarborough Dining';
    }
  }

  ngOnInit(): void {
    this.role = sessionStorage.getItem('role');
    this.userId = sessionStorage.getItem('userId');
  }

  ngAfterViewInit(): void {
    if (window.innerWidth < 650) {
      this.onResize();
    }
  }

  upgradeUser(): void {
    this.loginService.updateUser(this.auth.userProfile$.source);
    this.auth.role = 'RO';
  }

  reload() {
    sessionStorage.clear();
    window.location.reload();
  }

  browse() {
    this.router.navigate(['/all-listings']).then(() => {
      setTimeout(function () {
        window.location.reload();
      }, 100);
    });
  }

  timeline() {
    this.router.navigate(['/timeline']).then(() => {
      setTimeout(function () {
        window.location.reload();
      }, 100);
    });
  }
}
