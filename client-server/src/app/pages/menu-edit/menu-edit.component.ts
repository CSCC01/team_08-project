import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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

  faEdit = faEdit;
  faTrash = faTrash;

  deleteModalRef: any;
  dishModalRef: any;
  dishEdit: boolean = false;
  dishes: any[];
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
    private restaurantsService: RestaurantsService,
    private dishModalService: NgbModal,
    private deleteModalService: NgbModal
  ) {}

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.userId = this.route.snapshot.queryParams.userId;
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;

    if (!this.restaurantId || this.role !== 'RO') {
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

  openDishModal(content, dish?) {
    if (dish !== undefined) {
      this.dishId = dish._id;
      this.dishName = dish.name;
      this.price = dish.price;
      this.menuCategory = 'default'; //TODO: currently not accepted as input
      this.cuisine = 'default';
      this.dishInfo = dish.description;
      this.allergy = 'default';

      this.dishEdit = true;
    } else {
      this.clearInput();
    }

    this.dishModalRef = this.dishModalService.open(content, { size: 'xl' });
  }

  openDeleteModal(content, dish) {
    this.dishName = dish.name;
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
          this.restaurantsService.editDish(dishInfo);
        } else {
          this.restaurantsService.createDish(dishInfo);
        }

        this.clearInput();
        this.loadAllDishes();
        this.dishEdit = false;
        this.dishModalRef.close();
        this.loadAllDishes();
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
    this.clearInput();
    this.loadAllDishes();
    this.deleteModalRef.close();
    this.loadAllDishes();
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
}
