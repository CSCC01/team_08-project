import { TestBed } from '@angular/core/testing';

import { RoCheckGuard } from './ro-check.guard';

describe('RoCheckGuard', () => {
  let guard: RoCheckGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(RoCheckGuard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
