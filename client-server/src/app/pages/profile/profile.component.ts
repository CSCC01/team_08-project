import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { LoginService } from 'src/app/service/login.service';
import { faCalendar } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  userId: string = '';
  userData: any;
  modalRef: any;
  faCalendar = faCalendar;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public auth: AuthService,
    private loginService: LoginService,
    private modalService: NgbModal
  ) {}

  ngOnInit() {
    this.userId = sessionStorage.getItem('userId');
    this.getUserInfo();
  }

  openEditModal(content) {
    this.modalRef = this.modalService.open(content);
  }

  updateProfile() {
    var userInfo = {
      email: this.userId,
      name: (<HTMLInputElement>document.getElementById('name')).value,
      address: (<HTMLInputElement>document.getElementById('address')).value,
      phone: (<HTMLInputElement>document.getElementById('phone')).value,
      birthday: (<HTMLInputElement>document.getElementById('dateOfBirth'))
        .value,
    };

    if (userInfo.birthday == '') {
      userInfo.birthday = null;
    }
    if (userInfo.phone == '') {
      userInfo.phone = null;
    }

    if (
      (userInfo.phone != null && userInfo.phone.length != 10) ||
      (userInfo.birthday != null &&
        !userInfo.birthday.match('^\\d{4}-\\d{2}-\\d{2}$')) ||
      !userInfo.name
    ) {
      alert(
        'Please ensure formats are proper. Name should not empty, phone numbers should be 10 digits with no dashes and birthday should be YYYY-MM-DD'
      );
    } else {
      this.loginService.editUser(userInfo);
      this.modalRef.close();
      this.getUserInfo();
      setTimeout(function () {
        window.location.reload();
      });
    }
  }

  getUserInfo() {
    this.loginService.getUser({ email: this.userId }).subscribe((data) => {
      this.userData = data;
    });
  }
}
