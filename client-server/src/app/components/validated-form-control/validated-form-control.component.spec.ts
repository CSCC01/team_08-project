import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ValidatedFormControlComponent } from './validated-form-control.component';

describe('ValidatedFormControlComponent', () => {
  let component: ValidatedFormControlComponent;
  let fixture: ComponentFixture<ValidatedFormControlComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ValidatedFormControlComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ValidatedFormControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
