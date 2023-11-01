import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from 'src/app/services/login.service';
import * as alertify from 'alertifyjs';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  public loginForm!: FormGroup;

  constructor(private service: LoginService, 
    private router: Router) {}

  ngOnInit(): void {
    this.initLoginForm();
  }

  private initLoginForm(): void {
    this.loginForm = new FormGroup({
      username: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
    });
  }

  get username() {
    return this.loginForm.controls['username'];
  }

  get password() {
    return this.loginForm.controls['password'];
  }

  // Login a user
  onLogin() {
    const username = this.username.value;
    const password = this.password.value;
    
    // Create form data and append the values
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
  
    this.service.onLogin(formData).subscribe(
      (response: any) => {
        const token = response.access_token;
        if (token) {
          localStorage.setItem('token', token);
          alertify.success('Login Successful');
          this.router.navigate(['/home']);
        } else {
          alertify.error('Login Failed');
          this.router.navigate(['/login']);
        }
      }
    );
  }
  
}
