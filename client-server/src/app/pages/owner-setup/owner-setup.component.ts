import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-owner-setup',
  templateUrl: './owner-setup.component.html',
  styleUrls: ['./owner-setup.component.scss'],
})
export class OwnerSetupComponent implements OnInit {
  restaurantId: string = '';

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    if (!this.restaurantId) {
      this.router.navigate(['']);
    }
  }

  updateOwner() {
    this.router.navigate(['/menu-setup'], {
      queryParams: { restaurantId: this.restaurantId },
    });
  }
}
