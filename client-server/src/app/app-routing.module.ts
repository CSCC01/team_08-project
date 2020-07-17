import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProfileComponent } from './pages/profile/profile.component';
import { AuthGuard } from './auth/auth.guard';
import { HomeComponent } from './pages/home/home.component';
import { PaymentComponent } from './pages/payment/payment.component';
import { AllRestaurantsComponent } from './pages/all-restaurants/all-restaurants.component';
import { RestaurantPageComponent } from './pages/restaurant-page/restaurant-page.component';
import { RestuarantDashboardComponent } from './pages/restuarant-dashboard/restuarant-dashboard.component';
import { RestaurantSetupComponent } from './pages/restaurant-setup/restaurant-setup.component';
import { OwnerSetupComponent } from './pages/owner-setup/owner-setup.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  {
    path: 'profile',
    component: ProfileComponent,
    canActivate: [AuthGuard],
  },
  { path: 'payment', component: PaymentComponent },
  { path: 'all-listings', component: AllRestaurantsComponent },
  { path: 'restaurant', component: RestaurantPageComponent },
  { path: 'dashboard', component: RestuarantDashboardComponent },
  { path: 'restaurant-setup', component: RestaurantSetupComponent },
  { path: 'owner-setup', component: OwnerSetupComponent },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      scrollPositionRestoration: 'enabled', // Add options right here
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
