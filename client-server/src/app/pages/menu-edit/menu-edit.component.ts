import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
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
        var dishInfo = {
          _id: this.dishId,
          name: this.dishName,
          restaurant_id: this.restaurantId,
          description: this.dishInfo,
          picture:
            'https://www.bbcgoodfood.com/sites/default/files/recipe-collections/collection-image/2013/05/chorizo-mozarella-gnocchi-bake-cropped.jpg',
          price: price.toFixed(2),
          specials: '',
        };

        if (this.dishEdit) {
          this.restaurantsService.editDish(dishInfo).subscribe((data) => {
            this.dishes[this.dishIndex] = data;
            this.dishIndex = 0;
          });
        } else {
          this.restaurantsService.createDish(dishInfo).subscribe((data) => {
            this.dishes.push(data);
          });
        }

        this.clearInput();
        this.dishEdit = false;
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
    this.router.navigate(['/restaurant']);
  }
}
