import { TestBed } from '@angular/core/testing';

import { RoSetupGuard } from './ro-setup.guard';

describe('RoSetupGuard', () => {
  let guard: RoSetupGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(RoSetupGuard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
