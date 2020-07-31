import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { DataService } from 'src/app/service/data.service';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import { RestaurantsService } from 'src/app/service/restaurants.service';

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
    private data: DataService,
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder,
    private restaurantsService: RestaurantsService,
    private dishModalService: NgbModal,
    private deleteModalService: NgbModal
  ) {}

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.userId = this.route.snapshot.queryParams.userId;
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;

    if (!this.restaurantId || this.role !== 'RO' || !this.userId) {
      this.router.navigate([''], {
        queryParams: {
          role: this.role,
          userId: this.userId,
          restaurantId: this.restaurantId,
        },
      });
      alert('No matching restaurant found for this profile!');
    }
    this.data.changeRestaurantId(this.restaurantId);
    this.data.changeUserId(this.userId);
    this.data.changeRole(this.role);
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
      this.menuCategory = 'default'; //TODO: currently not accepted as input
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
        //TODO: picture currently defaulted, will be changed when Google Cloud is implemented
        var dishInfo = {};
        dishInfo['_id'] = this.dishId;
        dishInfo['name'] = this.dishName;
        dishInfo['restaurant_id'] = this.restaurantId;
        dishInfo['description'] = this.dishInfo;
        dishInfo['price'] = price.toFixed(2);
        dishInfo['specials'] = '';

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
      } else {
        alert('Please enter a valid price!');
      }
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
    this.router.navigate(['/restaurant'], {
      queryParams: {
        role: this.role,
        userId: this.userId,
        restaurantId: this.restaurantId,
      },
    });
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
