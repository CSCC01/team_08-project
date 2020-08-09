import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { formValidation } from "../../validation/forms";
import { dishValidator } from '../../validation/dishValidator';
import { formValidator } from '../../validation/formValidator';

@Component({
  selector: 'app-menu-edit',
  templateUrl: './menu-edit.component.html',
  styleUrls: ['./menu-edit.component.scss'],
})
export class MenuEditComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';

  uploadForm: FormGroup;
  validator: formValidator = new dishValidator();
  newImage: boolean = false;

  faEdit = faEdit;
  faTrash = faTrash;

  deleteModalRef: any;
  dishModalRef: any;
  dishEdit: boolean = false;
  dishes: any[];
  dishIndex: number;

  dishId: string = '';
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
    private dishModalService: NgbModal,
    private deleteModalService: NgbModal
  ) {}

  ngOnInit(): void {
    this.role = sessionStorage.getItem('role');
    this.userId = sessionStorage.getItem('userId');
    this.restaurantId = sessionStorage.getItem('restaurantId');

    if (!this.restaurantId || this.role !== 'RO' || !this.userId) {
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

  clearInput() {
    this.dishId = '';
    this.dishName = '';
    this.price = '';
    this.menuCategory = '';
    this.cuisine = '';
    this.dishInfo = '';
    this.allergy = '';
  }

  openDishModal(content, dish?, index?) {
    if (dish !== undefined) {
      // dish edit
      this.dishId = dish._id;
      this.dishName = dish.name;
      this.price = dish.price;
      this.menuCategory = dish.category;
      this.cuisine = 'default';
      this.dishInfo = dish.description;
      this.allergy = 'default';

      this.dishEdit = true;
      this.dishIndex = index;
    } else {
      this.clearInput();
    }

    this.dishModalRef = this.dishModalService.open(content, { size: 'xl' });
  }

  openDeleteModal(content, dish, index) {
    this.dishName = dish.name;
    this.dishIndex = index;
    this.deleteModalRef = this.deleteModalService.open(content, { size: 's' });
  }

  configDish() {

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

    if ( ! failFlag
    ) {
        const price: number = +this.price;
        var dishInfo = {};
        dishInfo['_id'] = this.dishId;
        dishInfo['name'] = this.dishName;
        dishInfo['restaurant_id'] = this.restaurantId;
        dishInfo['description'] = this.dishInfo;
        dishInfo['price'] = price.toFixed(2);
        dishInfo['category'] = this.menuCategory;
        dishInfo['specials'] = '';
        dishInfo['category'] = this.menuCategory;

        if (this.dishEdit) {
          this.restaurantsService.editDish(dishInfo).subscribe((data) => {
            if (this.newImage) {
              this.onSubmit(data._id);
            } else {
              this.dishes[this.dishIndex] = data;
              this.dishIndex = 0;
              this.dishEdit = false;
            }
          });
        } else {
          dishInfo['picture'] = '';
          this.restaurantsService.createDish(dishInfo).subscribe((data) => {
            if (this.newImage) {
              this.onSubmit(data._id);
            } else {
              this.dishes.push(data);
            }
          });
        }

        this.clearInput();
        this.dishModalRef.close();
    }
  }

  deleteDish() {
    var dishInfo = {
      food_name: this.dishName,
      restaurant_id: this.restaurantId,
    };

    this.restaurantsService.deleteDish(dishInfo);

    if (this.dishIndex > -1) {
      this.dishes.splice(this.dishIndex, 1);
    }

    this.clearInput();
    this.dishIndex = 0;
    this.deleteModalRef.close();
  }

  back() {
    this.router.navigate(['/restaurant']);
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
      if (this.dishEdit) {
        this.dishes[this.dishIndex] = data;
        this.dishIndex = 0;
      } else {
        this.dishes.push(data);
      }
      this.dishEdit = false;
    });

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
    this.newImage = false;
  }
}
