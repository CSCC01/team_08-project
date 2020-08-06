import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllOwnersComponent } from './all-owners.component';

describe('AllOwnersComponent', () => {
  let component: AllOwnersComponent;
  let fixture: ComponentFixture<AllOwnersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllOwnersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllOwnersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
