import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { AuthService } from '../../auth/auth.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { LoginService } from 'src/app/service/login.service';
import { faCalendar } from '@fortawesome/free-solid-svg-icons';
import { formError } from '../../utils/forms';

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

//   holds the error labels' states (this is where the labels get them from @Input)
  errors = {
    'name': '',
    'address': '',
    'phone': '',
    'birthday': ''
  }

//   conveniece function which causes an error label with the given fieldname to error
//   look at utils.formError.userConst to modify the error text
  formError(fieldName: string){
    this.errors[fieldName] = formError.userErrorConst[fieldName];
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
    sessionStorage.setItem('userAddress', userInfo.address);

    if (userInfo.birthday == '') {
      userInfo.birthday = null;
    }
    if (userInfo.phone == '') {
      userInfo.phone = null;
    }

    formError.clearErrors(this.errors);
    if (
      !formError.isPhoneValid(userInfo.phone) ||
      !formError.isBirthdayValid(userInfo.birthday) ||
      !userInfo.name || !userInfo.address
    ) {
        if(!formError.isBirthdayValid(userInfo.birthday)) this.formError('birthday');
        if(!formError.isPhoneValid(userInfo.phone)) this.formError('phone');
        if(!userInfo.address) this.formError('address');
        if(!userInfo.name) this.formError('name');
    } else {
      
      this.loginService.editUser(userInfo).subscribe((data) => {
        //if response is invalid, populate the errors
        if(formError.isInvalidResponse(data)){
            formError.HandleInvalid(data, this.formError)
        }else{
          if (this.newImage) {
            this.onSubmit();
          }
          else{
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
