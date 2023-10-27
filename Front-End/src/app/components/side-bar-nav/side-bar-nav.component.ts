import { Component, OnInit } from '@angular/core';
import jwtDecode from 'jwt-decode';
import { LoginService } from 'src/app/services/login.service';
import * as alertify from 'alertifyjs'

@Component({
  selector: 'app-side-bar-nav',
  templateUrl: './side-bar-nav.component.html',
  styleUrls: ['./side-bar-nav.component.css']
})
export class SideBarNavComponent implements OnInit{
  loggedInUser: any;

  constructor(private service: LoginService) {}

  ngOnInit() {
    this.loadLoggedInUser();
    this.isLoggedIn();
  }

  loadLoggedInUser() {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken: any = jwtDecode(token);
      this.service.getUserInfo(decodedToken).subscribe(
        (user: any) => {
          this.loggedInUser = user.logged_in_as;
        }
      );
    }
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  onLogout() {
    localStorage.removeItem('token');
    alertify.success("You have been logged out")
  }
}
