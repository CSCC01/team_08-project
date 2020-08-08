import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { RestaurantsService } from '../../service/restaurants.service';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { formValidation } from "../../validation/forms";
import { dishValidator } from '../../validation/dishValidator';
import { formValidator } from '../../validation/formValidator';

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
  validator: formValidator = new dishValidator();
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

    // only used for form validation
    var validationInfo = {
        name: this.dishName,
        price: this.price,
        menuCategory: this.menuCategory,
        cuisine: this.cuisine,
        dishInfo: this.dishInfo,
        allergy: this.allergy
    }

    this.validator.clearAllErrors();
    let failFlag = this.validator.validateAll(validationInfo, (key) => this.validator.setError(key));

    if ( ! failFlag) {

        const price: number = +this.price;

        var dishInfo = {
            name: this.dishName,
            restaurant_id: this.restaurantId,
            description: this.dishInfo,
            category: this.menuCategory,
            picture: '',
            price: price.toFixed(2),
            specials: '',
          };

        this.restaurantsService.createDish(dishInfo).subscribe((data) => {
            if(data && formValidation.isInvalidResponse(data)){
                formValidation.HandleInvalid(data, (key) => this.validator.setError(key))
            }else{
                if (this.newImage) {
                    this.onSubmit(data._id);
                }else{
                    this.dishes.push(data);
                    this.dishName = '';
                    this.price = '';
                    this.menuCategory = '';
                    this.cuisine = '';
                    this.dishInfo = '';
                    this.allergy = '';
                }
                this.modalRef.close();
          }
        });


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
