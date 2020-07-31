import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { DataService } from 'src/app/service/data.service';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-owner-setup',
  templateUrl: './owner-setup.component.html',
  styleUrls: ['./owner-setup.component.scss'],
})
export class OwnerSetupComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';

  uploadForm: FormGroup;
  newImage: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder,
    private data: DataService,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    this.userId = this.route.snapshot.queryParams.userId;
    this.role = this.route.snapshot.queryParams.role;

    if (!this.restaurantId || this.role !== 'RO' || !this.userId) {
      this.router.navigate([''], {
        queryParams: {
          role: this.role,
          userId: this.userId,
          restaurantId: this.restaurantId,
        },
      });
      alert('No matching restaurant found for this profile!');
    } else {
      this.data.changeRestaurantId(this.restaurantId);
      this.data.changeUserId(this.userId);
      this.data.changeRole(this.role);
    }

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
  }

  updateOwner() {
    var restaurantInfo = {
      restaurant_id: this.restaurantId,
      owner_name: (<HTMLInputElement>document.getElementById('owner-name'))
        .value,
      owner_story: (<HTMLInputElement>document.getElementById('owner-story'))
        .value,
    };
    if (restaurantInfo.owner_name == '' || restaurantInfo.owner_story == '') {
      alert('Please enter all requried information about the owner!');
    } else {
      this.restaurantsService.editRestaurant(restaurantInfo);
      if (this.newImage) {
        this.onSubmit();
      }
      this.router.navigate(['/menu-setup'], {
        queryParams: {
          role: this.role,
          userId: this.userId,
          restaurantId: this.restaurantId,
        },
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

  onSubmit() {
    const formData = new FormData();
    formData.append('file', this.uploadForm.get('file').value);
    this.restaurantsService
      .uploadRestaurantMedia(formData, this.restaurantId, 'owner')
      .subscribe((data) => {});
    this.newImage = false;
  }
}
