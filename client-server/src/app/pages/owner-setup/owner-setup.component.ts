import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from 'src/app/service/data.service';

@Component({
  selector: 'app-owner-setup',
  templateUrl: './owner-setup.component.html',
  styleUrls: ['./owner-setup.component.scss'],
})
export class OwnerSetupComponent implements OnInit {
  restaurantId: string = '';
  role: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private data: DataService
  ) {}

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    this.role = this.route.snapshot.queryParams.role;
    if (!this.restaurantId || this.role !== 'RO') {
      this.router.navigate([''], {
        queryParams: { role: this.role, restaurantId: this.restaurantId },
      });
      alert('No matching restaurant found for this profile!');
    } else {
      this.data.changeRestaurantId(this.restaurantId);
      this.data.changeRole(this.role);
    }
  }

  updateOwner() {
    this.router.navigate(['/menu-setup'], {
      queryParams: { role: this.role, restaurantId: this.restaurantId },
    });
  }
}
