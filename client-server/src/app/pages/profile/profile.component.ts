import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../auth/auth.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { LoginService } from 'src/app/service/login.service';
import { faCalendar } from '@fortawesome/free-solid-svg-icons';
import { formValidation } from '../../validation/forms';
import { userValidator } from '../../validation/userValidator';
import { formValidator } from '../../validation/formValidator';

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

  uploadForm: FormGroup;
  newImage: boolean = false;
  validator: formValidator = new userValidator();

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public auth: AuthService,
    private loginService: LoginService,
    private modalService: NgbModal,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit() {
    this.userId = sessionStorage.getItem('userId');
    this.getUserInfo();

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
  }
  openEditModal(content) {
    this.modalRef = this.modalService.open(content);
  }

  updateProfile() {
    let birthday = (<HTMLInputElement>document.getElementById('dateOfBirth'))
      .value;

    var userInfo = {
      email: this.userId,
      name: (<HTMLInputElement>document.getElementById('name')).value,
      address: (<HTMLInputElement>document.getElementById('address')).value,
      phone: (<HTMLInputElement>document.getElementById('phone')).value,
      birthday: birthday,
      age: birthday,
    };
    sessionStorage.setItem('userAddress', userInfo.address);

    // clear formErrors
    this.validator.clearAllErrors();
    //validate all formfields, the callback will throw appropriate errors, return true if any validation failed
    let failFlag = this.validator.validateAll(userInfo, (key) =>
      this.validator.setError(key)
    );
    //if any validation failed, do not POST
    if (!failFlag) {
      this.loginService.editUser(userInfo).subscribe((data) => {
        //if response is invalid, populate the errors
        if (data && formValidation.isInvalidResponse(data)) {
          formValidation.HandleInvalid(data, (key) =>
            this.validator.setError(key)
          );
        } else {
          if (this.newImage) {
            this.onSubmit();
          } else {
            this.modalRef.close();
            setTimeout(function () {
              window.location.reload();
            }, 100);
          }
          this.getUserInfo();
        }
      });
    }
  }

  getUserInfo() {
    this.loginService.getUser({ email: this.userId }).subscribe((data) => {
      this.userData = data;
    });
  }

  viewAllOrders() {
    this.router.navigate(['all-transactions']);
  }

  onFileSelect(event) {
    if (event.target.files.length > 0) {
      this.newImage = true;
      const file = event.target.files[0];
      this.uploadForm.get('file').setValue(file);
    }
  }

  onSubmit() {
    const formData = new FormData();
    formData.append('file', this.uploadForm.get('file').value);
    this.loginService
      .uploadUserMedia(formData, this.userId)
      .subscribe((data) => {
        this.newImage = false;
        setTimeout(function () {
          window.location.reload();
        });
      });
  }
}
