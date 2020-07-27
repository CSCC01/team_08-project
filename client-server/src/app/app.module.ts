import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { DishCardComponent } from './components/dish-card/dish-card.component';
import { OwnerCardComponent } from './components/owner-card/owner-card.component';
import { CarouselComponent } from './components/carousel/carousel.component';
import { FilterlistCardComponent } from './components/filterlist-card/filterlist-card.component';
import { ReviewCardComponent } from './components/review-card/review-card.component';
import { RestaurantCardComponent } from './components/restaurant-card/restaurant-card.component';

import { RatingModule } from 'ng-starrating';
import { CarouselModule } from 'ngx-bootstrap/carousel';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { MatTabsModule } from '@angular/material/tabs';
import { NumberPickerModule } from 'ng-number-picker';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { HomeComponent } from './pages/home/home.component';
import { PaymentComponent } from './pages/payment/payment.component';
import { RestaurantPageComponent } from './pages/restaurant-page/restaurant-page.component';

import { LoginService } from './service/login.service';
import { DataService } from './service/data.service';
import { ViewReviewCardComponent } from './components/view-review-card/view-review-card.component';
import { AllRestaurantsComponent } from './pages/all-restaurants/all-restaurants.component';
import { OrderCardComponent } from './components/order-card/order-card.component';
import { RestuarantDashboardComponent } from './pages/restuarant-dashboard/restuarant-dashboard.component';
import { RestaurantSetupComponent } from './pages/restaurant-setup/restaurant-setup.component';
import { OwnerSetupComponent } from './pages/owner-setup/owner-setup.component';
import { MenuSetupComponent } from './pages/menu-setup/menu-setup.component';
import { MenuEditComponent } from './pages/menu-edit/menu-edit.component';
import { OwnerEditComponent } from './pages/owner-edit/owner-edit.component';
import { RestaurantEditComponent } from './pages/restaurant-edit/restaurant-edit.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    ProfileComponent,
    DishCardComponent,
    OwnerCardComponent,
    CarouselComponent,
    HomeComponent,
    FilterlistCardComponent,
    ReviewCardComponent,
    RestaurantCardComponent,
    PaymentComponent,
    RestaurantPageComponent,
    ViewReviewCardComponent,
    AllRestaurantsComponent,
    OrderCardComponent,
    RestuarantDashboardComponent,
    RestaurantSetupComponent,
    OwnerSetupComponent,
    MenuSetupComponent,
    MenuEditComponent,
    OwnerEditComponent,
    RestaurantEditComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    FontAwesomeModule,
    RatingModule,
    CarouselModule.forRoot(),
    MatTabsModule,
    NumberPickerModule,
    NgbModule,
  ],
  providers: [LoginService, DataService],
  bootstrap: [AppComponent],
})
export class AppModule {}
