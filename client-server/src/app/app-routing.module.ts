import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProfileComponent } from './pages/profile/profile.component';
import { AuthGuard } from './auth/auth.guard';
import { ROCheckGuard } from './auth/ro-check.guard';
import { HomeComponent } from './pages/home/home.component';
import { PaymentComponent } from './pages/payment/payment.component';
import { AllRestaurantsComponent } from './pages/all-restaurants/all-restaurants.component';
import { RestaurantPageComponent } from './pages/restaurant-page/restaurant-page.component';
import { RestuarantDashboardComponent } from './pages/restuarant-dashboard/restuarant-dashboard.component';
import { RestaurantSetupComponent } from './pages/restaurant-setup/restaurant-setup.component';
import { OwnerSetupComponent } from './pages/owner-setup/owner-setup.component';
import { MenuSetupComponent } from './pages/menu-setup/menu-setup.component';
import { MenuEditComponent } from './pages/menu-edit/menu-edit.component';
import { TimelineComponent } from './pages/timeline/timeline.component';
import { OwnerEditComponent } from './pages/owner-edit/owner-edit.component';
import { RestaurantEditComponent } from './pages/restaurant-edit/restaurant-edit.component';
import { CheckoutComponent } from './pages/checkout/checkout.component';
import { FavouritesComponent } from './pages/favourites/favourites.component';
import { AllOwnersComponent } from './pages/all-owners/all-owners.component';

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
  {
    path: 'dashboard',
    component: RestuarantDashboardComponent,
    canActivate: [ROCheckGuard],
  },
  { path: 'restaurant-setup', component: RestaurantSetupComponent },
  { path: 'owner-setup', component: OwnerSetupComponent },
  { path: 'menu-setup', component: MenuSetupComponent },
  { path: 'menu-edit', component: MenuEditComponent },
  { path: 'timeline', component: TimelineComponent },
  { path: 'owner-edit', component: OwnerEditComponent },
  { path: 'restaurant-edit', component: RestaurantEditComponent },
  { path: 'checkout', component: CheckoutComponent },
  { path: 'favourites', component: FavouritesComponent },
  { path: 'all-owners', component: AllOwnersComponent },
  { path: '**', redirectTo: '' },
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
