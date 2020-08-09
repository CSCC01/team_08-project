import {
  Component,
  OnInit,
  HostListener,
  ViewChild,
  TemplateRef,
  AfterViewInit,
} from '@angular/core';
import AOS from 'aos';
import 'aos/dist/aos.css';
import {
  faArrowCircleUp,
  faArrowCircleDown,
  faCalendar,
} from '@fortawesome/free-solid-svg-icons';
import { AuthService } from 'src/app/auth/auth.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { LoginService } from '../../service/login.service';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { formValidation } from "../../validation/forms";
import { userValidator } from '../../validation/userValidator';
import { formValidator } from '../../validation/formValidator';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit, AfterViewInit {
  role: string = '';
  userId: string = '';
  userData: any;

  validator: formValidator = new userValidator();

  isShow: boolean;
  topPosToStartShowing = 100;
  faArrowCircleUp = faArrowCircleUp;
  faArrowCircleDown = faArrowCircleDown;
  arrowsOutside = true;
  faCalendar = faCalendar;

  @ViewChild('userInfo', { static: true }) content: TemplateRef<any>;
  modalRef: any;

  totalStars: number = 5;
  dishes: any[] = [];
  stories: any[] = [];

  cuisines = [
    {
      type: 'image',
      path: 'assets/images/cuisines/chinese.jpg',
      caption: 'Chinese',
    },
    {
      type: 'image',
      path: 'assets/images/cuisines/greek.jpg',
      caption: 'Greek',
    },
    {
      type: 'image',
      path: 'assets/images/cuisines/indian.jpg',
      caption: 'Indian',
    },
    {
      type: 'image',
      path: 'assets/images/cuisines/italian.jpg',
      caption: 'Italian',
    },
    {
      type: 'image',
      path: 'assets/images/cuisines/japanese.jpg',
      caption: 'Japanese',
    },
    { type: 'image', path: 'assets/images/cuisines/thai.jpg', caption: 'Thai' },
    {
      type: 'image',
      path: 'assets/images/cuisines/vietnamese.jpg',
      caption: 'Vietnamese',
    },
  ];

  constructor(
    public auth: AuthService,
    private route: ActivatedRoute,
    private modalService: NgbModal,
    private router: Router,
    private loginService: LoginService,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {
    AOS.init({
      delay: 300,
      duration: 1500,
      once: false,
      anchorPlacement: 'top-bottom',
    });

    this.restaurantsService.getDishes().subscribe((data) => {
      const len = data.Dishes.length < 5 ? data.Dishes.length : 5;
      for (let i = 0; i < len; i++) {
        data.Dishes[i].type = 'dish';
        this.dishes[i] = data.Dishes[i];
      }
    });

    this.restaurantsService.listRestaurants().subscribe((data) => {
      const len = data.Restaurants.length < 5 ? data.Restaurants.length : 5;
      for (let i = 0; i < len; i++) {
        this.stories[i] = {
          type: 'story',
          name: data.Restaurants[i].owner_name,
          profile_pic: data.Restaurants[i].owner_picture_url,
          bio: data.Restaurants[i].owner_story,
          restaurant: data.Restaurants[i].name,
          _id: data.Restaurants[i]._id,
        };
      }
    });

    this.userId = sessionStorage.getItem('userId');
    this.role = sessionStorage.getItem('role');

    if (this.userId.length > 0 && this.role == 'BU') {
      this.loginService.getUser({ email: this.userId }).subscribe((data) => {
        this.userData = data;

        if (!data.birthday || !data.address || !data.phone) {
          this.modalRef = this.modalService.open(this.content);
        }
      });
    }
  }

  ngAfterViewInit(): void {
    if (window.innerWidth < 850) {
      this.onResize();
    }
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.arrowsOutside = window.innerWidth < 1250 ? false : true;

    if (window.innerWidth < 850) {
      var el = document.getElementsByClassName(
        'overview-section'
      ) as HTMLCollectionOf<HTMLElement>;
      for (var i = 0; i < el.length; i++) {
        el[i].classList.remove('row');
      }
    } else {
      var el = document.getElementsByClassName(
        'overview-section'
      ) as HTMLCollectionOf<HTMLElement>;
      for (var i = 0; i < el.length; i++) {
        if (!el[i].classList.contains('row')) {
          el[i].classList.add('row');
        }
      }
    }
  }

  @HostListener('window:scroll')
  checkScroll() {
    const scrollPosition =
      window.pageYOffset ||
      document.documentElement.scrollTop ||
      document.body.scrollTop ||
      0;

    if (scrollPosition >= this.topPosToStartShowing) {
      this.isShow = true;
    } else {
      this.isShow = false;
    }
  }

  gotoTop() {
    window.scroll({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  }

  scrollDown() {
    const newPosition = document.getElementById('scroll').offsetTop;
    window.scroll({
      top: newPosition,
      left: 0,
      behavior: 'smooth',
    });
  }

  browseListings() {
    this.router.navigate(['/all-listings']);
  }

  browseStories() {
    this.router.navigate(['/all-owners']);
  }

  updateProfile() {

    let birthday = (<HTMLInputElement>document.getElementById('dateOfBirth')).value

    var userInfo = {
      email: this.userId,
      name: (<HTMLInputElement>document.getElementById('name')).value,
      address: (<HTMLInputElement>document.getElementById('address')).value,
      phone: (<HTMLInputElement>document.getElementById('phone')).value,
      birthday: birthday,
      age: birthday
    };

    sessionStorage.setItem('userAddress', userInfo.address);

    // clear formErrors
    this.validator.clearAllErrors();
    //validate all formfields, the callback will throw appropriate errors, return true if any validation failed
    let failFlag = this.validator.validateAll(userInfo, (key) => this.validator.setError(key));
    //if any validation failed, do not POST
    if (!failFlag) {
      this.loginService.editUser(userInfo).subscribe((data) => {
        //if response is invalid, populate the errors
        if(formValidation.isInvalidResponse(data)){
            formValidation.HandleInvalid(data, (key) => this.validator.setError(key))
        }else{
            this.modalRef.close();
            setTimeout(function () {
            window.location.reload();
            }, 100);
        }
      });

    }
  }
}
