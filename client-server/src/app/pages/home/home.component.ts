import {
  Component,
  OnInit,
  HostListener,
  ViewChild,
  TemplateRef,
} from '@angular/core';
import AOS from 'aos';
import 'aos/dist/aos.css';
import {
  faArrowCircleUp,
  faArrowCircleDown,
  faCalendar,
} from '@fortawesome/free-solid-svg-icons';
import dishes from '../../../assets/data/dishes.json';
import stories from '../../../assets/data/stories.json';
import { AuthService } from 'src/app/auth/auth.service';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from 'src/app/service/data.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { LoginService } from '../../service/login.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';
  userInfo: any;

  isShow: boolean;
  topPosToStartShowing = 100;
  faArrowCircleUp = faArrowCircleUp;
  faArrowCircleDown = faArrowCircleDown;
  arrowsOutside = true;
  faCalendar = faCalendar;

  @ViewChild('userInfo', { static: true }) content: TemplateRef<any>;
  modalRef: any;

  totalStars: number = 5;
  dishes: any[];
  stories: any[];

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
    private data: DataService,
    private route: ActivatedRoute,
    private modalService: NgbModal,
    private router: Router,
    private loginService: LoginService
  ) {
    this.dishes = dishes;
    this.stories = stories;
  }

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.userId = this.route.snapshot.queryParams.userId;
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;

    this.data.changeRestaurantId(this.restaurantId);
    this.data.changeUserId(this.userId);
    this.data.changeRole(this.role);

    AOS.init({
      delay: 300,
      duration: 1500,
      once: false,
      anchorPlacement: 'top-bottom',
    });

    if (this.userId.length > 0) {
      console.log(this.userId);
      this.loginService.getUser({ email: this.userId }).subscribe((data) => {
        this.userInfo = data;
        if (!data.birhtday || !data.address || !data.phone) {
          console.log('Goes in here!');
          this.modalRef = this.modalService.open(this.content);
        }
      });
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

  updateProfile() {
    var userInfo = {
      email: this.userId,
      name: (<HTMLInputElement>document.getElementById('name')).value,
      address: (<HTMLInputElement>document.getElementById('address')).value,
      phone: (<HTMLInputElement>document.getElementById('phone')).value,
      birthday: (<HTMLInputElement>document.getElementById('dateOfBirth'))
        .value,
    };
    this.loginService.editUser(userInfo);
    this.modalRef.close();
  }
}
