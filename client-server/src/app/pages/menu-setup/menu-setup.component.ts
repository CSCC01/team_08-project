import { Component, OnInit } from '@angular/core';
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
  role: string = '';

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
    private restaurantsService: RestaurantsService,
    private modalService: NgbModal
  ) {}

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    this.role = this.route.snapshot.queryParams.role;
    this.loadAllDishes();
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
        //TODO: picture currently defaulted, will be changed when Google Cloud is implemented
        var dishInfo = {
          name: this.dishName,
          restaurant_id: this.restaurantId,
          description: this.dishInfo,
          picture:
            'https://www.bbcgoodfood.com/sites/default/files/recipe-collections/collection-image/2013/05/chorizo-mozarella-gnocchi-bake-cropped.jpg',
          price: price.toFixed(2),
          specials: '',
        };

        this.restaurantsService.createDish(dishInfo);

        this.dishName = '';
        this.price = '';
        this.menuCategory = '';
        this.cuisine = '';
        this.dishInfo = '';
        this.allergy = '';

        this.modalRef.close();
        this.loadAllDishes();
      } else {
        alert('Please enter a valid price!');
      }
    }
  }
}
