import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RestuarantDashboardComponent } from './restuarant-dashboard.component';

describe('RestuarantDashboardComponent', () => {
  let component: RestuarantDashboardComponent;
  let fixture: ComponentFixture<RestuarantDashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RestuarantDashboardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RestuarantDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
