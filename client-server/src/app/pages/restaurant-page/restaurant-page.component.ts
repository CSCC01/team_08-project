import { Component, OnInit, Input, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import {
  faMapMarkerAlt,
  faPhone,
  faEdit,
  faShippingFast,
} from '@fortawesome/free-solid-svg-icons';
import { faHeart, faEnvelope } from '@fortawesome/free-regular-svg-icons';
import { faTwitter, faInstagram } from '@fortawesome/free-brands-svg-icons';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ReviewsService } from 'src/app/service/reviews.service';
import { LoginService } from '../../service/login.service';

@Component({
  selector: 'app-restaurant-page',
  templateUrl: './restaurant-page.component.html',
  styleUrls: ['./restaurant-page.component.scss'],
})
export class RestaurantPageComponent implements OnInit {
  restaurantId: string = '';
  role: string = '';
  userId: string = '';
  error: boolean = false;

  headerModalRef: any;
  reviewModalRef: any;
  uploadForm: FormGroup;
  newImage: boolean = false;

  dishes: any[] = [];
  reviews: any[] = [];
  restaurantDetails: any;
  restaurantMenu: any[] = [];

  totalStars = 5;
  faMapMarker = faMapMarkerAlt;
  faPhone = faPhone;
  faMail = faEnvelope;
  faHeartLine = faHeart;
  faTwitter = faTwitter;
  faInstagram = faInstagram;
  faEdit = faEdit;
  faShippingFast = faShippingFast;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private restaurantsService: RestaurantsService,
    private reviewService: ReviewsService,
    private loginService: LoginService,
    private headerModalService: NgbModal,
    private reviewModalService: NgbModal,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.restaurantId =
      this.route.snapshot.queryParams.restaurantId ||
      sessionStorage.getItem('restaurantId');
    this.role = sessionStorage.getItem('role');
    this.userId = sessionStorage.getItem('userId');

    // generate restaurant page
    this.restaurantsService.getRestaurant(this.restaurantId).subscribe(
      (data) => {
        this.restaurantDetails = data;
      },
      (error) => {
        this.error = true;
      }
    );

    // generate restaurant menu
    this.restaurantsService
      .getRestaurantFood(this.restaurantId)
      .subscribe((data) => {
        this.restaurantMenu = data.Dishes;
      });

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });

    // generate restaurant reviews
    this.getReview();
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    var el1 = document.getElementById('info-col1');
    var el2 = document.getElementById('info-col2');
    var el3 = document.getElementById('info-row');

    if (window.innerWidth < 750) {
      el1.classList.remove('col-md-7');
      el2.classList.remove('col-md-5');
      el3.classList.remove('row');
    } else {
      el1.classList.add('col-md-7');
      el2.classList.add('col-md-5');
      el3.classList.add('row');
    }
  }

  viewTimeline() {
    this.router.navigate(['/timeline'], {
      queryParams: {
        restaurantId: this.restaurantId,
        updates: true,
      },
    });
  }

  editMenu() {
    this.router.navigate(['/menu-edit']);
  }

  editOwner() {
    this.router.navigate(['/owner-edit']);
  }

  editRestaurant() {
    this.router.navigate(['/restaurant-edit']);
  }

  openEditHeaderModal(content) {
    this.headerModalRef = this.headerModalService.open(content, { size: 's' });
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
    this.restaurantsService
      .uploadRestaurantMedia(formData, this.restaurantId, 'cover')
      .subscribe((data) => {
        this.newImage = false;
        window.location.reload();
      });
    this.headerModalRef.close();
  }

  openReviewModal(content) {
    this.reviewModalRef = this.reviewModalService.open(content, { size: 'm' });
  }

  addReview(review) {
    review.restaurant_id = this.restaurantId;
    review.user_email = this.userId;
    this.reviewService.insertReview(review).subscribe((data) => {});
    this.reviewModalRef.close();
    setTimeout(function () {
      window.location.reload();
    }, 100);
  }

  getReview() {
    this.reviews = [];
    this.reviewService
      .getReviewbyRestaurant(this.restaurantId)
      .subscribe((data) => {
        this.reviews = data.Reviews;
        this.getReviewerInfo();
      });
  }

  getReviewerInfo() {
    for (let i = 0; i < this.reviews.length; i++) {
      this.loginService
        .getUser({ email: this.reviews[i].user_email })
        .subscribe((data) => {
          this.reviews[i].reviewer = data.name;
          this.reviews[i].reviewer_image = data.picture;
        });
    }
  }
}
