import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { RestaurantsService } from '../../service/restaurants.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-menu-setup',
  templateUrl: './menu-setup.component.html',
  styleUrls: ['./menu-setup.component.scss'],
})
export class MenuSetupComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';

  uploadForm: FormGroup;
  newImage: boolean = false;

  modalRef: any;
  dishes: any[];
  dishName: string = '';
  price: string = '';
  menuCategory: string = '';
  cuisine: string = '';
  dishInfo: string = '';
  allergy: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder,
    private restaurantsService: RestaurantsService,
    private modalService: NgbModal
  ) {}

  ngOnInit(): void {
    this.restaurantId = sessionStorage.getItem('restaurantId');
    this.userId = sessionStorage.getItem('userId');
    this.role = sessionStorage.getItem('role');

    if (!this.restaurantId || !this.userId) {
      this.router.navigate(['']);
      alert('No matching restaurant found for this profile!');
    }

    this.loadAllDishes();

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
  }

  loadAllDishes() {
    this.restaurantsService
      .getRestaurantFood(this.restaurantId)
      .subscribe((data) => {
        this.dishes = data.Dishes;
      });
  }

  openAddDish(content) {
    this.modalRef = this.modalService.open(content, { size: 'xl' });
  }

  addDish() {
    if (
      this.dishName == '' ||
      this.price == '' ||
      this.menuCategory == '' ||
      this.cuisine == '' ||
      this.dishInfo == '' ||
      this.allergy == ''
    ) {
      alert('Please enter requried information about the dish!');
    } else {
      if (!isNaN(Number(this.price))) {
        const price: number = +this.price;
        var dishInfo = {
          name: this.dishName,
          restaurant_id: this.restaurantId,
          description: this.dishInfo,
          picture: '',
          price: price.toFixed(2),
          specials: '',
          category: this.menuCategory,
        };

        this.restaurantsService.createDish(dishInfo).subscribe((data) => {
          if (this.newImage) {
            this.onSubmit(data._id);
          } else {
            this.dishes.push(data);
          }
        });

        this.dishName = '';
        this.price = '';
        this.menuCategory = '';
        this.cuisine = '';
        this.dishInfo = '';
        this.allergy = '';

        this.modalRef.close();
      } else {
        alert('Please enter a valid price!');
      }
    }
  }

  onFileSelect(event) {
    if (event.target.files.length > 0) {
      this.newImage = true;
      const file = event.target.files[0];
      this.uploadForm.get('file').setValue(file);
    }
  }

  onSubmit(id: string) {
    const formData = new FormData();
    formData.append('file', this.uploadForm.get('file').value);
    this.restaurantsService.uploadFoodMedia(formData, id).subscribe((data) => {
      this.dishes.push(data);
    });

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });

    this.newImage = false;
  }

  goToHome() {
    this.router.navigate(['/']).then(() => {
      setTimeout(function () {
        window.location.reload();
      }, 1000);
    });
  }
}
