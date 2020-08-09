import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllOrderCardComponent } from './all-order-card.component';

describe('AllOrderCardComponent', () => {
  let component: AllOrderCardComponent;
  let fixture: ComponentFixture<AllOrderCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllOrderCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllOrderCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
