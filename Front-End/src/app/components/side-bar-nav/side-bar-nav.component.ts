import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-side-bar-nav',
  templateUrl: './side-bar-nav.component.html',
  styleUrls: ['./side-bar-nav.component.css']
})
export class SideBarNavComponent implements OnInit{

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.isLoginPage = this.router.url === '/login'; // Adjust the route to your actual login route
  }

  isLoginPage: any;
}
