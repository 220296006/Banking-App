import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  username!: string;
  constructor(private http: HttpClient) { }

  authenticateUser(user: any) {
    let userArray = [];
    if (localStorage.getItem('users')) {
      userArray = JSON.parse(localStorage.getItem('users') as string);
    }
    const authenticatedUser = userArray.find((p: { username: any; password: any; }) =>
      p.username === user.username && p.password === user.password);

    if (authenticatedUser) {
      // Store the authenticated user's data in local storage
      localStorage.setItem('authenticatedUser', JSON.stringify(authenticatedUser));
    }

    return authenticatedUser;
  }

  getAuthenticatedUser() {
    const authenticatedUserData = localStorage.getItem('authenticatedUser');
    if (authenticatedUserData) {
      return JSON.parse(authenticatedUserData);
    } else {
      return null;
    }
  }
}
