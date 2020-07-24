import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  UrlTree,
} from '@angular/router';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AuthService } from './auth.service';
import { DataService } from '../service/data.service';

@Injectable({
  providedIn: 'root',
})
export class ROCheckGuard implements CanActivate {
  constructor(private auth: AuthService, private data: DataService) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ):
    | Observable<boolean | UrlTree>
    | Promise<boolean | UrlTree>
    | boolean
    | UrlTree {
    return this.data.role.pipe(
      map((role) => {
        return role == 'RO';
      })
    );
  }
}
