import { Component, OnInit, HostListener, AfterViewInit } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import {
  faUserCircle,
  faMapMarkerAlt,
} from '@fortawesome/free-solid-svg-icons';
import { LoginService } from '../../service/login.service';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit, AfterViewInit {
  title: string = 'Find Dining Scarborough';

  restaurantId: string = '';
  role: string = '';
  userId: string = '';
  userAddress: string = '';

  modalRef: any;

  faUserCircle = faUserCircle;
  faMapMarkerAlt = faMapMarkerAlt;
  userRole: any;

  constructor(
    public auth: AuthService,
    private loginService: LoginService,
    private router: Router,
    private modalService: NgbModal
  ) {}

  @HostListener('window:resize', ['$event'])
  onResize() {
    if (window.innerWidth < 650) {
      this.title = 'SDining';
    } else {
      this.title = 'Find Dining Scarborough';
    }
  }

  ngOnInit(): void {
    this.role = sessionStorage.getItem('role');
    this.userId = sessionStorage.getItem('userId');
    this.userAddress = sessionStorage.getItem('userAddress');
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

  owners() {
    this.router.navigate(['/all-owners']).then(() => {
      setTimeout(function () {
        window.location.reload();
      }, 100);
    });
  }

  favourites() {
    this.router.navigate(['/favourites']).then(() => {
      setTimeout(function () {
        window.location.reload();
      }, 100);
    });
  }

  profile() {
    this.router.navigate(['/profile']).then(() => {
      setTimeout(function () {
        window.location.reload();
      }, 100);
    });
  }

  openModal(content) {
    this.modalRef = this.modalService.open(content, { size: 's' });
  }

  goToSetup() {
    this.modalRef.close();
  }
}
