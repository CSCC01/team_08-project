import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OwnerSetupComponent } from './owner-setup.component';

describe('OwnerSetupComponent', () => {
  let component: OwnerSetupComponent;
  let fixture: ComponentFixture<OwnerSetupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OwnerSetupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OwnerSetupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
